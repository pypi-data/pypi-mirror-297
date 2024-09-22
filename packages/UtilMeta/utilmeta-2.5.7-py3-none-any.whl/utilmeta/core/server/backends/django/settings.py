import django
import os
import sys
from typing import Union, List
from utilmeta import UtilMeta
from utilmeta.utils import import_obj
from utilmeta.conf.base import Config
from utilmeta.conf.time import Time
from utilmeta.core.orm.databases import DatabaseConnections, Database
from utilmeta.core.cache.config import CacheConnections, Cache

DEFAULT_MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    # "django.contrib.auth.middleware.AuthenticationMiddleware",
    # "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # utilmeta middleware
    # 'utilmeta.adapt.server.backends.django.DebugCookieMiddleware'
]
DEFAULT_APPS = [
    # "django.contrib.admin",
    # "django.contrib.auth",
    "django.contrib.contenttypes",
    # "django.contrib.sessions",
    # "django.contrib.messages",
    # "django.contrib.staticfiles",
]
DEFAULT_DB_ENGINE = {
    'sqlite': 'django.db.backends.sqlite3',
    'oracle': 'django.db.backends.oracle',
    'mysql': 'django.db.backends.mysql',
    'postgres': 'django.db.backends.postgresql'
}
WSGI_APPLICATION = "WSGI_APPLICATION"
ASGI_APPLICATION = "ASGI_APPLICATION"
ROOT_URLCONF = "ROOT_URLCONF"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SETTINGS_MODULE = 'DJANGO_SETTINGS_MODULE'
DEFAULT_LANGUAGE_CODE = "en-us"
DEFAULT_TIME_ZONE = "UTC"
DEFAULT_USE_I18N = True
DEFAULT_USE_TZ = True

DB = 'django.core.cache.backends.db.DatabaseCache'
FILE = 'django.core.cache.backends.filebased.FileBasedCache'
DUMMY = 'django.core.cache.backends.dummy.DummyCache'
LOCMEM = 'django.core.cache.backends.locmem.LocMemCache'
MEMCACHED = 'django.core.cache.backends.memcached.MemcachedCache'
PYLIBMC = 'django.core.cache.backends.memcached.PyLibMCCache'
DJANGO_REDIS = 'django.core.cache.backends.redis.RedisCache'
CACHE_BACKENDS = {
    'db': DB,
    'database': DB,
    'file': FILE,
    'locmem': LOCMEM,
    'memcached': MEMCACHED,
    'redis': DJANGO_REDIS,
    'pylibmc': PYLIBMC
}


class DjangoSettings(Config):
    def __init__(
            self,
            module_name: str = None, *,
            # current settings module for django project
            root_urlconf: str = None,
            # current url conf (if there is an exists django project)
            secret_key: str = None,
            apps_package: str = None,
            # package ref (such as 'domain' / 'service.applications')
            apps: Union[tuple, List[str]] = (),
            database_routers: tuple = (),
            allowed_hosts: list = (),
            middleware: Union[tuple, List[str]] = (),
            default_autofield: str = None,
            wsgi_application: str = None,
            # time_zone: str = None,
            # use_tz: bool = None,
            user_i18n: bool = None,
            language: str = None,
            append_slash: bool = False,
            extra: dict = None,
            # urlpatterns: list = None,
    ):
        super().__init__(**locals())
        self.module_name = module_name
        self.secret_key = secret_key
        self.apps_package = apps_package
        self.apps = list(apps)
        self.allowed_hosts = allowed_hosts
        self.middleware = middleware
        self.root_urlconf = root_urlconf
        self.default_autofield = default_autofield
        self.wsgi_application = wsgi_application
        # self.time_zone = DEFAULT_TIME_ZONE if time_zone is None else time_zone
        # self.use_tz = DEFAULT_USE_TZ if use_tz is None else use_tz
        self.language = DEFAULT_LANGUAGE_CODE if language is None else language
        self.use_i18n = DEFAULT_USE_I18N if user_i18n is None else user_i18n
        self.append_slash = append_slash
        self.module = None
        self.url_conf = None
        self.database_routers = list(database_routers)
        # self.urlpatterns = urlpatterns
        self._settings = {}
        self._extra_settings = extra
        self._plugin_settings = {}

        self.load_apps()

    def register(self, plugin):
        getter = getattr(plugin, 'as_django', None)
        if callable(getter):
            plugin_settings = getter()
            if not isinstance(plugin_settings, dict):
                raise TypeError(f'Invalid settings: {plugin_settings}')
            self._plugin_settings.update(plugin_settings)
            if self.module:
                # already set
                self._settings.update(plugin_settings)
                from django.conf import settings
                for attr, value in plugin_settings.items():
                    setattr(self.module, attr, value)
                    setattr(settings, attr, value)

    @property
    def apps_path(self):
        if not self.apps_package:
            return None
        package = import_obj(self.apps_package)
        return package.__path__[0]

    @classmethod
    def app_labels(cls) -> List[str]:
        from django.apps.registry import apps
        labels = []
        for key, cfg in apps.app_configs.items():
            labels.append(cfg.label)
        return labels

    def get_db(self, app_label: str):
        # TODO
        return 'default'

    def get_secret(self, service: UtilMeta):
        if self.secret_key:
            return self.secret_key
        # generate a stable random secret based on the path, this could be insecure
        # if the attacker happen to guess the key
        import platform
        import hashlib
        import warnings
        import utilmeta
        if service.production:
            raise ValueError(f'django: secret_key not set for production')
        else:
            warnings.warn('django: secret_key not set, auto generating')
        tag = f'{service.name}:{service.description}:{service.version}' \
              f'{service.backend_name}:{service.module_name}' \
              f'{django.__version__}{utilmeta.__version__}{sys.version}{platform.platform()}'.encode()
        return hashlib.sha256(tag).hexdigest()

    def load_apps(self):
        installed_apps = list(DEFAULT_APPS)
        installed_apps.extend(self.apps)

        if self.apps_package:
            apps_path = self.apps_path
            hosted_labels = [p for p in next(os.walk(apps_path))[1] if '__' not in p]
            for app in hosted_labels:
                label = f'{self.apps_package}.{app}'
                if label not in installed_apps:
                    installed_apps.append(label)

        self.apps = installed_apps
        return installed_apps

    @classmethod
    def get_cache(cls, cache: Cache):
        return {
            'BACKEND': CACHE_BACKENDS.get(cache.engine) or cache.engine,
            'LOCATION': cache.get_location(),
            'OPTIONS': cache.options or {},
            'KEY_FUNCTION': cache.key_function,
            'KEY_PREFIX': cache.prefix,
            'TIMEOUT': cache.timeout,
            'MAX_ENTRIES': cache.max_entries,
        }

    @classmethod
    def get_database(cls, db: Database, service: UtilMeta):
        engine = db.engine
        if '.' not in db.engine:
            for name, eg in DEFAULT_DB_ENGINE.items():
                if name.lower() in engine.lower():
                    if name == 'postgres' and service.asynchronous and django.VERSION >= (4, 2):
                        # COMPAT DJANGO > 4.2
                        engine = 'utilmeta.core.server.backends.django.postgresql'
                    else:
                        engine = eg
                    break

        options = {}
        if db.ssl:
            options['sslmode'] = 'require'
        if 'sqlite' in engine:
            return {
                'ENGINE': engine,
                'NAME': db.name,
                'OPTIONS': options
            }
        return {
            'ENGINE': engine,
            'HOST': db.host,
            'PORT': db.port,
            'NAME': db.name,
            'USER': db.user,
            'TIME_ZONE': db.time_zone,
            'PASSWORD': db.password,
            'CONN_MAX_AGE': db.max_age,
            'DISABLE_SERVER_SIDE_CURSORS': db.pooled,
            'OPTIONS': options
        }

    def hook(self, service: UtilMeta):
        from .cmd import DjangoCommand
        from .adaptor import DjangoServerAdaptor
        service.register_command(DjangoCommand)
        if isinstance(service.adaptor, DjangoServerAdaptor):
            service.adaptor.settings = self
            # replace settings

    def setup(self, service: UtilMeta):
        if self._settings:
            # already configured
            return

        # print('SETUP:', service.module, self.apps)
        # from utilmeta.ops.config import Operations
        # ops_config = service.get_config(Operations)
        # if ops_config:
        #     ops_config.setup(service)
        #     return

        if self.module_name:
            module = sys.modules[self.module_name]
        else:
            module = service.module
            self.module_name = service.module_name

        self.module = module
        db_config = service.get_config(DatabaseConnections)
        cache_config = service.get_config(CacheConnections)
        databases = {}
        caches = {}

        if db_config:
            from utilmeta.core.orm.backends.django.database import DjangoDatabaseAdaptor
            for name, db in db_config.databases.items():
                if not db.sync_adaptor_cls:
                    db.sync_adaptor_cls = DjangoDatabaseAdaptor
                databases[name] = self.get_database(db, service)

        if cache_config:
            from utilmeta.core.cache.backends.django import DjangoCacheAdaptor
            for name, cache in cache_config.caches.items():
                if not cache.sync_adaptor_cls:
                    cache.sync_adaptor_cls = DjangoCacheAdaptor
                caches[name] = self.get_cache(cache)

        middleware = list(self.middleware or DEFAULT_MIDDLEWARE)
        adaptor = service.adaptor
        from .adaptor import DjangoServerAdaptor
        if isinstance(adaptor, DjangoServerAdaptor):
            middleware_func = adaptor.middleware_func
            if middleware_func:
                setattr(self.module, middleware_func.__name__, middleware_func)
                middleware.append(f'{self.module_name}.{middleware_func.__name__}')

        hosts = list(self.allowed_hosts)
        if service.origin:
            from urllib.parse import urlparse
            hosts.append(urlparse(service.origin).hostname)

        settings = {
            'DEBUG': not service.production,
            'SECRET_KEY': self.get_secret(service),
            'BASE_DIR': service.project_dir,
            'MIDDLEWARE': middleware,
            'INSTALLED_APPS': self.apps,
            'ALLOWED_HOSTS': hosts,
            'DATABASE_ROUTERS': self.database_routers,
            'APPEND_SLASH': self.append_slash,
            'LANGUAGE_CODE': self.language,
            'USE_I18N': self.use_i18n,
            'DEFAULT_AUTO_FIELD': self.default_autofield or DEFAULT_AUTO_FIELD,
            # 'DATABASES': databases,
            # 'CACHES': caches,
            ROOT_URLCONF: self.root_urlconf or service.module_name,
            WSGI_APPLICATION: self.wsgi_application or f'{service.module_name}.app',
        }

        if databases:
            settings.update({'DATABASES': databases})
        if caches:
            settings.update({'CACHES': caches})

        time_config = Time.config()
        if time_config:
            settings.update({
                'DATETIME_FORMAT': time_config.datetime_format,
                'DATE_FORMAT': time_config.date_format,
                'TIME_ZONE': time_config.time_zone or DEFAULT_TIME_ZONE,
                'USE_TZ': time_config.use_tz,
            })
        else:
            # mandatory
            settings.update({
                'TIME_ZONE': DEFAULT_TIME_ZONE,
                'USE_TZ': True,
            })

        if self._plugin_settings:
            settings.update(self._plugin_settings)
        if isinstance(self._extra_settings, dict):
            settings.update(self._extra_settings)

        self._settings = settings
        for attr, value in settings.items():
            setattr(module, attr, value)

        os.environ[SETTINGS_MODULE] = self.module_name or service.module_name
        # not using setdefault to prevent IDE set the wrong value by default
        django.setup(set_prefix=False)

        # import root url conf after the django setup
        if self.root_urlconf:
            self.url_conf = sys.modules.get(self.root_urlconf) or import_obj(self.root_urlconf)
        else:
            self.url_conf = service.module

        urlpatterns = getattr(self.url_conf, 'urlpatterns', [])
        # if self.urlpatterns:
        #     urlpatterns = urlpatterns + self.urlpatterns
        setattr(self.url_conf, 'urlpatterns', urlpatterns or [])

    @property
    def wsgi_module_ref(self):
        wsgi_app_ref = self._settings.get(WSGI_APPLICATION)
        if isinstance(wsgi_app_ref, str) and '.' in wsgi_app_ref:
            return '.'.join(wsgi_app_ref.split('.')[:-1])
        return None

    @property
    def wsgi_app_attr(self):
        wsgi_app_ref = self._settings.get(WSGI_APPLICATION)
        if isinstance(wsgi_app_ref, str) and '.' in wsgi_app_ref:
            return wsgi_app_ref.split('.')[-1]
        return None

    @property
    def wsgi_module(self):
        wsgi_module_ref = self.wsgi_module_ref
        if wsgi_module_ref:
            # if module_ref == self.module_name:
            #     return self.module
            try:
                return import_obj(wsgi_module_ref)
            except (ModuleNotFoundError, ImportError):
                return None
        return None

    @property
    def wsgi_app(self):
        wsgi_app_ref = self._settings.get(WSGI_APPLICATION)
        if wsgi_app_ref:
            try:
                return import_obj(wsgi_app_ref)
            except (ModuleNotFoundError, ImportError):
                return None
        return None
