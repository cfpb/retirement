from __future__ import absolute_import

from .standalone import *

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'CRITICAL',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
        }
    }
}
