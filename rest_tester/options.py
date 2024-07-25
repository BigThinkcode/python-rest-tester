"""
This file contains Options class with its properties
"""

from rest_tester.logger import logger

class Options:
    def __init__(self, options):
        self.options = options

    @property
    def base_url(self):
        return self.options['http_request_settings'].get('base_url')
    
    @property
    def verify_ssl(self):
        return self.options['http_request_settings'].get('verify_ssl', True)
    
    @property
    def dir_groups_to_test(self):
        return self.options['execution_settings']['dir_groups_to_test']
    
    @property
    def auto_convert(self):
        return self.options['execution_settings'].get('auto_convert', False)
    
    @property
    def authentication_configs(self):
        return self.options['auth_settings']
    
    @property
    def users(self):
        return self.options['user_tokens']
    
    @property
    def request_method(self):
        return self.options['http_request_settings'].get('method', 'basic')
    
    @property
    def default_test_settings(self):
        return self.options['default_test_settings']