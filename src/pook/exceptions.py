import warnings


class PookInvalidBody(Exception):
    pass


class PookNoMatches(Exception):
    pass


class PookNetworkFilterError(Exception):
    pass


class PookExpiredMock(Exception):
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "PookExpiredMock is deprecated and will be removed in a future version of Pook",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)


class PookInvalidArgument(Exception):
    pass
