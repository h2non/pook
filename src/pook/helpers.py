import re
from inspect import isfunction, ismethod

from .exceptions import PookInvalidArgument

reply_response_re = re.compile("^(response|reply)_")


def _get_key(key_order):
    def key(x):
        raw = reply_response_re.sub("", x)
        try:
            return key_order.index(raw)
        except KeyError:
            raise PookInvalidArgument(f"Unsupported argument: {x}")

    return key


def trigger_methods(instance, args, key_order=None):
    """
    Triggers specific class methods using a simple reflection
    mechanism based on the given input dictionary params.

    Arguments:
        instance (object): target instance to dynamically trigger methods.
        args (iterable): input arguments to trigger objects to
        key_order (None|iterable): optional order in which to process keys; falls back to `sorted`'s default behaviour if not present

    Returns:
        None
    """
    # Start the magic
    if key_order:
        key = _get_key(key_order)
        sorted_args = sorted(args, key=key)
    else:
        sorted_args = sorted(args)

    for name in sorted_args:
        value = args[name]
        target = instance

        # If response attibutes
        if reply_response_re.match(name):
            name = reply_response_re.sub("", name)
            # If instance has response attribute, use it
            if hasattr(instance, "_response"):
                target = instance._response

        # Retrieve class member for inspection and future use
        member = getattr(target, name, None)

        # Is attribute
        isattr = name in dir(target)
        iscallable = ismethod(member) and not isfunction(member)

        if not iscallable and not isattr:
            raise PookInvalidArgument(f"Unsupported argument: {name}")

        # Set attribute or trigger method
        if iscallable:
            member(value)
        else:
            setattr(target, name, value)
