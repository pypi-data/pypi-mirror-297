import os

from jdlib.exceptions import ImproperlyConfigured


class Env:
    ENVIRON = os.environ

    def __init__(self):
        pass

    def __call__(self, var, cast=None, default=None):
        return self.get_value(var, cast=cast, default=default)

    def __contains__(self, var):
        return var in self.ENVIRON
    
    def get_value(self, var, cast=None, default=None):
        try:
            value = self.ENVIRON[var]
        except KeyError as e:
            if default is None:
                raise ImproperlyConfigured(f'{var} environment variable is not set.') from e
            value = default

        return self.cast_value(value, cast=cast)
    
    def bool(self, var, default=None):
        return self.__call__(var, bool, default)
    
    def list(self, var, default=None):
        return self.__call__(var, list, default)

    def cast_value(self, value, cast=None):
        if cast is None:
            return value

        if cast is bool:
            try:
                value = int(value) != 0
            except ValueError:
                value = value.lower() in ['true', '1']
        elif cast is list:
            value = [x for x in value.split(',') if x]

        return value
