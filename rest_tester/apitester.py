"""
This file contains APITester class with its properties and methods
"""

import os

from rest_tester.logger import logger
from rest_tester.options import Options
from rest_tester.modules.auth_module import Authenticator
from rest_tester.modules.request_module import get_api_client
from rest_tester.utils.postman_parser import convert_from_postman
from rest_tester.utils.openapi_parser import convert_from_openapi
from rest_tester.configs.constants import openapi_id_name, postman_id_name
from rest_tester.utils.utils import *


class APITester:

    def __init__(self, configs: dict) -> None:
        self.config = Options(configs) 

    def split_test_folder_directory(self, tests_groups_directory: str) -> list:
        """
        Method to split given tests folder path to list of possible combinations
        :param:
            tests_groups_directory: Path of the folder which has the test json file
        :returns:
            List of possible combinations of paths
        """
        parts = tests_groups_directory.rstrip('/').split('/')
        return ['/'.join(parts[:i + 1]) + '/' for i in range(len(parts))]
    
    def get_dir_groups_to_test(self, tests_groups_directory: str) -> str:
        """
        Method to check the given test groups directory to parse other formats if any
        :param:
            tests_groups_directory: Path of the folder which has the test json file
        :returns:
            Path of test groups directory after parsing
        """
        with open(tests_groups_directory, 'r') as file:
            if tests_groups_directory.endswith('.yaml'):
                file_content = yaml.safe_load(file)
            elif tests_groups_directory.endswith('.json'):
                file_content = json.load(file)
        if postman_id_name in list(file_content.get('info', {})):
            return convert_from_postman(tests_groups_directory)
        elif openapi_id_name in list(file_content):
            return convert_from_openapi(tests_groups_directory)
        else:
            return tests_groups_directory
    
    def read_test_groups(self) -> dict:
        """
        Recursively reads JSON files inside the given root folder and sub-folders.
        :returns:
            Dictionary with tests folder path as key and list of dicts as value
        tests_metadata sample dict:
            {
                '1/': [{test json},{test json}]},
                '1/2/': [{test json},{test json}]},
                '1/3/': [{test json},{test json}]}
            }
        """
        json_folder_files = {}
        if os.path.exists(self.config.dir_groups_to_test) or os.path.isfile(self.config.dir_groups_to_test):
            logger.info("Directory exists. Reading Directory contents...")
            dir_groups_to_test = self.get_dir_groups_to_test(self.config.dir_groups_to_test) if self.config.auto_convert else self.config.dir_groups_to_test
            dir_groups_to_test = dir_groups_to_test + '/' if dir_groups_to_test[-1] != '/' else dir_groups_to_test
            for subdir, dirs, files in os.walk(dir_groups_to_test):
                for filename in files:
                    filepath = os.path.join(subdir, filename)
                    if filepath.endswith(".json"):
                        folder_path = os.path.dirname(filepath)
                        relative_folder_path = (
                            folder_path[len(dir_groups_to_test) :] + "/" if dir_groups_to_test else folder_path + "/"
                        )
                        jsons = read_json_file(filepath)
                        json_folder_files.update({relative_folder_path: jsons})
            logger.info("Directory contents read successfully.")
            return json_folder_files
        else:
            raise Exception("Directory does not exist or invalid folder path")

    def build_test_data(self) -> tuple:
        """
        Method to get the test_inputs and test_ids for all test JSONs.
        :returns:
            List of possible combinations of paths
        """
        test_ids = []
        test_inputs = []
        groups = self.read_test_groups()
        authenticator = Authenticator(self.config.authentication_configs, get_api_client(self.config))
        for user_config in self.config.users:
            user_groups = user_config['test_groups']
            user_token = user_config.get('token', '')
            authenticator.login(user_token)
            for group, test_info in groups.items():
                for user_group in user_groups:
                    if user_group in self.split_test_folder_directory(group):
                        for json in test_info:
                            api = json['api']
                            tests = json['tests']
                            authenticator.is_token_valid(user_token)
                            data = self.parse_request_payload(api.get('data', {}))
                            settings = {
                                        "params": api.get('params', {}),
                                        "json": data,
                                        }
                            api_response = authenticator.api_client.send_request(api['method'], api['uri'], **settings)
                            for test_type, expected_value in tests.items():
                                if expected_value:
                                    test_inputs.append((api_response, {"type": test_type, "value": expected_value}))
                                    test_ids.append(f"{group} - {api['uri']} - {test_type}")
            authenticator.logout()
        return test_ids, test_inputs
    
    def parse_request_payload(self, data: str | dict) -> dict:
        """
        Method to parse the request payload, if it is based on data model class
        :param:
            data: String representation of class or normal dictionary
        :returns:
            returns desired payload based on data model if found, else return input directly
        """
        if isinstance(data, str):
            class_name = data
            class_ = get_class(class_name, "rest_tester.tests.payloads")
            if class_:
                data = class_().model_dump(mode="json")
        return data