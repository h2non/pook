from .api import *  # noqa
from .api import __all__ as api_exports

# Delegate to API export
__all__ = api_exports

# Package metadata
__author__ = 'Tomas Aparicio'
__license__ = 'MIT'

# Current version
__version__ = '0.1.8'
