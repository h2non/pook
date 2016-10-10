from inspect import isfunction
from .exceptions import PookInvalidArgument

def trigger_methods(instance, args):
    """"
    Triggers the required class methods using simple reflection
    based on the given arguments dictionary.
    """
    for key, arg in args.items():
        method = getattr(instance, key, None)
        if isfunction(method):
            raise PookInvalidArgument('Unsupported argument: {}'.format(key))
        method(arg)
