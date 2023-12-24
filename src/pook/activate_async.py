import functools
from asyncio import iscoroutinefunction


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
    async def wrapper(*args, **kw):
        _engine.activate()
        try:
            if iscoroutinefunction(fn):
                async for v in fn(*args, **kw):
                    yield v
            else:
                fn(*args, **kw)
        finally:
            _engine.disable()

    return wrapper
