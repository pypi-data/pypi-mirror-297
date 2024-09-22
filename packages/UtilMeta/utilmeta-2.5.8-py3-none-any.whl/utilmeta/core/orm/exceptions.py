
class ModelRequired(ValueError):
    def __init__(self, msg: str = None):
        super().__init__(msg or 'orm.Error: model is required for query execution')


class MissingPrimaryKey(ValueError):
    def __init__(self, msg: str, model=None):
        self.model = model
        super().__init__(msg or 'orm.Error: pk is missing for update')


class UpdateFailed(ValueError):
    def __init__(self, msg: str, model=None):
        self.model = model
        super().__init__(msg or 'orm.Error: must_update=True: failed to update')


class EmptyQueryset(ValueError):
    def __init__(self, msg: str, model=None):
        self.model = model
        super().__init__(msg or 'orm.Error: result is empty')


class InvalidMode(TypeError):
    pass
