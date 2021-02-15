
USERS = {
    'REQ': {
        'username': 'U0177818',
        'password': '07855',
        'url': 'tcp://127.0.0.1:5560'
    },
    'SUB': {
        'username': 'U0177818',
        'password': '07855',
        'url': 'tcp://127.0.0.1:5561'
    }
}

USER_SETTINGS = {
    'CLIENT_CODE': "10744",
}

ACCOUNTS = {
    'fixed_term': "SPBFUT000yt", # Срочный
    'stock': "NL0011100043", # Фондовый
    'currency': "MB1000100002", # Валютный
}

FIRM_ID = {
    'fixed_term': "SPBFUT000000", # Срочный
    'stock': "NC0011100000", # Фондовый
    'currency': "MB1000100000", # Валютный
}

# TODO: Settings for logger
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': 'logs/qpc.log',
        },
        'errors': {
            'level': 'ERROR',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': 'logs/errors.log',
        },
        'connector': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': 'logs/connector.log',
        },
        'events': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': 'logs/events.log',
        },
        'trade': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': 'logs/trade.log',
        },
    },
    'loggers': {
        'default': {
            'handlers': ['default', 'errors'],
            'level': 'INFO',
        },
        'connector': {
            'handlers': ['connector', 'errors'],
            'level': 'INFO',
        },
        'events': {
            'handlers': ['events', 'errors'],
            'level': 'INFO',
        },
        'trade': {
            'handlers': ['trade', 'errors'],
            'level': 'INFO',
        },
    }
}
