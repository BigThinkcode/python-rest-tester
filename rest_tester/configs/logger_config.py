"""
Config file to be used by Application
config file will be loaded based on environment's
"""

from rest_tester.configs.configs import configs as cfg

config_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "1": {
            "format": "TIME:%(asctime)s - module:%(module)s - loglevel:%(levelname)s - logger:%(name)s - function:%(funcName)s() - line_no:%(lineno)-4d - message:%(message)s",
        },
        "2": {
            "format": "TIME:%(asctime)s - module:%(module)s - loglevel:%(levelname)s - logger:%(name)s - function:%(funcName)s() - message:%(message)s - call_trace:%(pathname)s - line_no:%(lineno)d",
        },
        "3": {
            "format": "[%(asctime)s]-[%(levelname)s]-[%(message)s]-ln:[%(lineno)-d] in %(module)s\n",
        },
    },
    "handlers": {
        "detailedConsoleHandler": {
            "class": "logging.StreamHandler",
            "level": cfg['execution_settings']['log_level'],
            "formatter": cfg['execution_settings']['log_format'],
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "rest_tester": {
            "level": cfg['execution_settings']['log_level'],
            "handlers": ["detailedConsoleHandler"],
        }
    },
}
