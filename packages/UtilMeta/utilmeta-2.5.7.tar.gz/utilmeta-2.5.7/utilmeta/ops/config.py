import inspect
import threading

from utilmeta.conf import Config
from utilmeta.core.orm.databases.config import Database, DatabaseConnections
from utype.types import *
from utilmeta.utils import DEFAULT_SECRET_NAMES, url_join, localhost, cached_property, import_obj
from typing import Union
from urllib.parse import urlsplit
from utilmeta import UtilMeta, __version__
from utilmeta.core import api
import sys
import hashlib


class Operations(Config):
    __eager__ = True
    # setup need to execute before django settings

    NAME = 'ops'
    REF = 'utilmeta.ops'
    HOST = 'utilmeta.com'
    ROUTER_NAME = '_OperationsDatabaseRouter'

    database = Database

    def __init__(self,
                 route: str,
                 database: Union[str, Database],
                 base_url: str = None,
                 # replace service.base_url
                 disabled_scope: List[str] = (),
                 secret_names: List[str] = DEFAULT_SECRET_NAMES,
                 trusted_hosts: List[str] = (),
                 default_timeout: int = 30,
                 secure_only: bool = True,
                 local_disabled: bool = False,
                 logger_cls=None,
                 max_backlog: int = 100,
                 # will trigger a log save if the log hits this limit
                 worker_cycle: Union[int, float, timedelta] = timedelta(seconds=30),
                 worker_task_cls=None,
                 # every worker cycle, a worker will do
                 # - save the logs
                 # - save the worker monitor
                 # - the main (with min pid) worker will do the monitor tasks
                 external_openapi: dict = None,     # openapi paths
                 max_retention_time: Union[int, float, timedelta] = timedelta(days=90),
                 ):
        super().__init__(**locals())

        self.route = route
        self.database = database if isinstance(database, Database) else None
        self.db_alias = database if isinstance(database, str) else '__ops'

        self.disabled_scope = set(disabled_scope)
        self.secret_names = [k.lower() for k in secret_names]
        self.trusted_hosts = list(trusted_hosts)
        self.default_timeout = default_timeout
        self.secure_only = secure_only
        self.local_disabled = local_disabled

        if isinstance(max_retention_time, timedelta):
            max_retention_time = max_retention_time.total_seconds()
        if isinstance(worker_cycle, timedelta):
            worker_cycle = worker_cycle.total_seconds()

        self.max_retention_time = max_retention_time
        self.worker_cycle = worker_cycle
        self.worker_task_cls_string = worker_task_cls
        self.max_backlog = max_backlog
        self._base_url = base_url

        if self.HOST not in self.trusted_hosts:
            self.trusted_hosts.append(self.HOST)

        self.logger_cls_string = logger_cls
        self._ready = False

    @cached_property
    def logger_cls(self):
        from utilmeta.ops.log import Logger
        if not self.logger_cls_string:
            return Logger
        cls = import_obj(self.logger_cls_string)
        if not issubclass(cls, Logger):
            raise TypeError(f'Operations.logger_cls must inherit utilmeta.ops.log.Logger, got {cls}')
        return cls

    @cached_property
    def worker_task_cls(self):
        from utilmeta.ops.task import OperationWorkerTask
        if not self.worker_task_cls_string:
            return OperationWorkerTask
        cls = import_obj(self.worker_task_cls_string)
        if not issubclass(cls, OperationWorkerTask):
            raise TypeError(f'Operations.worker_task_cls must inherit '
                            f'utilmeta.ops.task.OperationWorkerTask, got {cls}')
        return cls

    @classmethod
    def get_secret_key(cls, service: UtilMeta):
        seed = f'{service.module_name}:{service.name}:' \
               f'{service.backend_name}:{service.backend_version}:{service.base_url}:{__version__}:{sys.version}'
        return hashlib.md5(seed.encode()).hexdigest()

    def hook(self, service: UtilMeta):
        from .cmd import OperationsCommand
        service.register_command(OperationsCommand)

    def setup(self, service: UtilMeta):
        if self._ready:
            return

        # --- add log middleware
        if service.adaptor:
            service.adaptor.add_middleware(
                self.logger_cls.middleware_cls(self)
            )
        else:
            raise NotImplementedError('Operations setup error: service backend not specified')

        from utilmeta.core.server.backends.django.settings import DjangoSettings
        django_config = service.get_config(DjangoSettings)

        db_routers = []
        if self.db_alias != 'default':
            db_router = self.get_database_router()
            setattr(service.module, self.ROUTER_NAME, db_router)
            db_routers.append(f'{service.module_name}.{self.ROUTER_NAME}')

        if django_config:
            if self.REF not in django_config.apps:
                django_config.apps.append(self.REF)
            if db_routers:
                django_config.database_routers.extend(db_routers)
        else:
            django_config = DjangoSettings(
                apps=[self.REF],
                database_routers=tuple(db_routers),
                secret_key=self.get_secret_key(service),
            )
            service.use(django_config)

        # --------- DATABASE
        dbs_config = service.get_config(DatabaseConnections)
        if dbs_config:
            if self.database:
                dbs_config.add_database(
                    service=service,
                    alias=self.db_alias,
                    database=self.database
                )
            else:
                self.database = dbs_config.databases.get(self.db_alias)
                if not self.database:
                    raise ValueError(f'Operations config: database required, got invalid {repr(self.db_alias)}')
        else:
            if not self.database:
                raise ValueError(f'Operations config: database required, got invalid {repr(self.db_alias)}')
            service.use(DatabaseConnections({
                self.db_alias: self.database
            }))

        # setup here, before importing APIs
        django_config.setup(service)
        # ----------

        # -------------- API
        from utilmeta.ops.api import OperationsAPI
        parsed = urlsplit(self.route)
        if not parsed.scheme:
            # route instead of URL
            root_api = service.resolve()
            if not root_api:
                raise ValueError('OperationsAPI failed to load: no root API found in current service')

            if inspect.isclass(root_api) and issubclass(root_api, api.API):
                if not issubclass(root_api, OperationsAPI):
                    # mount the root API only
                    try:
                        root_api.__mount__(
                            OperationsAPI,
                            route=self.route,
                        )
                    except ValueError:
                        # if already exists, quit mounting
                        pass

        self._ready = True

    def on_startup(self, service):
        ops_api = self.ops_api
        if not ops_api:
            return
        print(f'UtilMeta operations API loaded at {ops_api}, '
              f'you can visit https://ops.utilmeta.com to manage your APIs')

        # from .log import setup_locals
        # threading.Thread(target=setup_locals, args=(self,)).start()

        # task
        task = self.worker_task_cls(self)
        thread = threading.Thread(target=task.start)
        thread.setDaemon(True)
        # todo: protect resources of daemon thread
        thread.start()
        # setup_locals(self)

    def get_database_router(self):
        class OperationsDatabaseRouter:
            @staticmethod
            def db_for_read(model, **hints):
                if model._meta.app_label == self.NAME:
                    return self.db_alias
                return None

            @staticmethod
            def db_for_write(model, **hints):
                if model._meta.app_label == self.NAME:
                    return self.db_alias
                return None

            @staticmethod
            def allow_relation(obj1, obj2, **hints):
                return None

            @staticmethod
            def allow_migrate(db, app_label, model_name=None, **hints):
                if app_label == self.NAME:
                    return db == self.db_alias
                else:
                    if db == self.db_alias:
                        return False
                    return None
        return OperationsDatabaseRouter

    @property
    def ops_api(self):
        parsed = urlsplit(self.route)
        if parsed.scheme:
            # is url
            return self.route
        return url_join(self.base_url, self.route)

    @property
    def base_url(self):
        if self._base_url:
            parsed = urlsplit(self._base_url)
            if parsed.scheme:
                return self._base_url
        try:
            from utilmeta import service
        except ImportError:
            return None
        return service.base_url

    def check_host(self):
        parsed = urlsplit(self.ops_api)
        if localhost(str(parsed.hostname)):
            return False
        return True

    def check_supervisor(self, base_url: str):
        parsed = urlsplit(base_url)
        if self.secure_only:
            if parsed.scheme not in ['https', 'wss']:
                raise ValueError(f'Insecure supervisor: {base_url}, '
                                 f'HTTPS is required, or you need to turn secure_only=False')
        host = str(parsed.hostname)
        for trusted in self.trusted_hosts:
            if host == trusted or host.endswith(f'.{trusted}'):
                return True
        raise ValueError(f'Untrusted supervisor host: {parsed.hostname}, if you trust this host, '
                         f'you need to add it to the [trusted_hosts] param of Operations config')

    @classmethod
    def get_backend_name(cls, backend):
        return getattr(backend, '__name__', '')

    def integrate(self, backend, module=None):
        from utilmeta import UtilMeta
        try:
            from utilmeta import service
        except ImportError:
            parsed = urlsplit(self.route)
            service = UtilMeta(
                module,
                backend=backend,
                name=self.get_backend_name(backend),
            )
            service.use(self)
            service.setup()
            # import API after setup
            if service.adaptor:
                from .api import OperationsAPI
                service.adaptor.adapt(Operations, route=parsed.path)
                service.adaptor.setup_middlewares()
            else:
                raise NotImplementedError('Operations integrate error: service backend not specified')

            if service.module:
                # ATTRIBUTE FINDER
                setattr(service.module, 'utilmeta', service)

    def is_secret(self, key: str):
        for k in self.secret_names:
            if k in key.lower():
                return True
        return False
