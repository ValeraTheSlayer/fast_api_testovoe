import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'DEBUG',  # Change to 'INFO' or 'ERROR' as needed
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console']
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
