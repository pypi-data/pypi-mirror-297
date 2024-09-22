import os

from jdlib.exceptions import ImproperlyConfigured


class Env:
    ENVIRON = os.environ

    def __init__(self):
        pass

    def __call__(self, var):
        return self.get_value(var)

    def __contains__(self, var):
        return var in self.ENVIRON
    
    def get_value(self, var):
        try:
            value = self.ENVIRON[var]
        except KeyError as e:
            raise ImproperlyConfigured(f'{var} environment variable is not set.') from e
        
        return value
