"""
This file configures the logger to be used as per Dictconfig inside configs
"""

import logging.config

from rest_tester.configs import logger_config

logging.config.dictConfig(logger_config.config_dict)
logger = logging.getLogger(__name__)
