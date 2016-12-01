from inspect import ismethod, isfunction
from .exceptions import PookInvalidArgument


def trigger_methods(instance, args):
    """"
    Triggers specific class methods using a simple reflection
    mechanism based on the given input dictionary params.

    Arguments:
        instance (object): target instance to dynamically trigger methods.
        args (iterable): input arguments to trigger objects to
    """
    # Start the magic
    for name in sorted(args):
        value = args[name]
        target = instance

        # If response attibutes
        if name.startswith('response_') or name.startswith('reply_'):
            name = name.replace('response_', '').replace('reply_', '')
            # If instance has response attribute, use it
            if hasattr(instance, '_response'):
                target = instance._response

        # Retrieve class member for inspection and future use
        member = getattr(target, name, None)

        # Is attribute
        isattr = name in dir(target)
        iscallable = ismethod(member) and not isfunction(member)

        if not iscallable and not isattr:
            raise PookInvalidArgument('Unsupported argument: {}'.format(name))

        # Set attribute or trigger method
        if iscallable:
            member(value)
        else:
            setattr(target, name, value)
