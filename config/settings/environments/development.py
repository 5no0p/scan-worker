from config.settings.components._base import (
    INSTALLED_APPS,
    MIDDLEWARE,
    BASE_DIR 
)

DEBUG = False

INSTALLED_APPS += [
    "debug_toolbar",
    "django_extensions",
    'graphiql_debug_toolbar',
]

INSTALLED_APPS = ["daphne",] + INSTALLED_APPS

MIDDLEWARE += [
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
    'graphiql_debug_toolbar.middleware.DebugToolbarMiddleware',
] 

INTERNAL_IPS = [
    "127.0.0.1",
]

LOGGING = {
    'version': 1,
    # The version number of our log
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{name} {levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',
        },
    },
    # django uses some of its own loggers for internal operations. In case you want to disable them just replace the False above with true.
    # A handler for WARNING. It is basically writing the WARNING messages into a file called WARNING.log
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'error.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    # A logger for WARNING which has a handler called 'file'. A logger can have multiple handler
    'loggers': {
       # notice the blank '', Usually you would put built in loggers like django or root here based on your needs
        '': {
            'handlers': ['file', 'console'], #notice how file variable is called in handler which has been defined above
            'level': 'DEBUG',
            'propagate': True,
        },
    },
    
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SHELL_PLUS_IMPORTS = [
    'from event import services, selector',
    'from event.graphql.v1 import queries, mutations, types, schema',
]