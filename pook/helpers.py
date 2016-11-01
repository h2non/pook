from inspect import ismethod, isfunction
from .exceptions import PookInvalidArgument


def trigger_methods(instance, args):
    """"
    Triggers specific class methods using a simple reflection
    mechanism based on the given input dictionary params.
    """
    for key, arg in args.items():
        method_name = key
        cls_instance = instance

        if key.startswith('response_'):
            method_name = key.replace('response_', '')
            cls_instance = instance.response

        method = getattr(cls_instance, method_name, None)
        if not ismethod(method) and not isfunction(method):
            raise PookInvalidArgument('Unsupported argument: {}'.format(key))

        method(arg)
