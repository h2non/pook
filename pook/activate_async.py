import functools
from inspect import isawaitable


def activate_async(fn, _engine):
    """
    Async version of activate decorator

    Arguments:
        fn (function): function that be wrapped by decorator.
        _engine (Engine): pook engine instance

    Returns:
        function: decorator wrapper function.
    """
    @functools.wraps(fn)
    async def wrapper(*args, **kw): # noqa
        _engine.activate()
        try:
            coro = fn(*args, **kw)
            if isawaitable(coro):
                await coro
        except Exception as err:
            raise err
        finally:
            _engine.disable()

    return wrapper
