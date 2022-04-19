import logging
from logging.config import dictConfig

import flask
from flask import request, current_app

from app.logging_config.log_formatters import RequestFormatter

log_con = flask.Blueprint('log_con', __name__)


@log_con.before_app_request
def before_request_logging():
    current_app.logger.info("Before Request")
    log = logging.getLogger("myApp")
    log.info("My App Logger")


@log_con.after_app_request
def after_request_logging(response):
    if request.path == '/favicon.ico':
        return response
    elif request.path.startswith('/static'):
        return response
    elif request.path.startswith('/bootstrap'):
        return response
    current_app.logger.info("After Request")

    log = logging.getLogger("myApp")
    log.info("My App Logger")
    log = logging.getLogger("myDebugs")
    log.info("My Debug Logger")
    log = logging.getLogger("myRequest")
    log.info("My Request Logger")
    return response


@log_con.before_app_first_request
def configure_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
    log = logging.getLogger("myApp")
    log.info("My App Logger")
    log = logging.getLogger("myErrors")
    log.info("THis broke")
    log = logging.getLogger("myDebugs")
    log.info("Debug logger")
    log = logging.getLogger("myRequests")
    log.info("Request logger")




LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'RequestFormatter': {
            '()': 'app.logging_config.log_formatters.RequestFormatter',
            'format': '[%(asctime)s] [%(process)d] %(remote_addr)s requested %(url)s'
                        '%(levelname)s in %(module)s: %(message)s'
        }
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'file.handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': 'app/logs/flask.log',
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.myApp': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': 'app/logs/myapp.log',
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.request': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'RequestFormatter',
            'filename': 'app/logs/request.log',
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.errors': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': 'app/logs/errors.log',
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.sqlalchemy': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': 'app/logs/sqlalchemy.log',
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.werkzeug': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': 'app/logs/werkzeug.log',
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.myDebugs': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'RequestFormatter',
            'filename': 'app/logs/debug.log',
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.myRequests': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'RequestFormatter',
            'filename': 'app/logs/requests.log',
            'maxBytes': 10000000,
            'backupCount': 5,

    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default','file.handler'],
            'level': 'DEBUG',
            'propagate': True
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['default','file.handler'],
            'level': 'DEBUG',
            'propagate': True
        },
        'werkzeug': {  # if __name__ == '__main__'
            'handlers': ['file.handler.werkzeug'],
            'level': 'DEBUG',
            'propagate': False
        },
        'sqlalchemy.engine': {  # if __name__ == '__main__'
            'handlers': ['file.handler.sqlalchemy'],
            'level': 'INFO',
            'propagate': False
        },
        'myApp': {  # if __name__ == '__main__'
            'handlers': ['file.handler.myApp'],
            'level': 'DEBUG',
            'propagate': False
        },
        'myErrors': {  # if __name__ == '__main__'
            'handlers': ['file.handler.errors'],
            'level': 'DEBUG',
            'propagate': False
        },
        'myDebugs': {  # if __name__ == '__main__'
            'handlers': ['file.handler.debug'],
            'level': 'DEBUG',
            'propagate': False
        },
        'myRequests': {  # if __name__ == '__main__'
            'handlers': ['file.handler.requests'],
            'level': 'DEBUG',
            'propagate': False
        },

    }
}
