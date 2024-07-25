"""
This file is the starting point of this application
"""

import jsonschema

import pytest
import json

from rest_tester.configs.configs import configs
from rest_tester.logger import logger
from rest_tester.apitester import APITester
from rest_tester.utils.utils import *


test_runner = APITester(configs)
test_ids, test_inputs = test_runner.build_test_data()

@pytest.mark.parametrize("response, test", test_inputs, ids=test_ids)
def test_api(response, test, request):
    """
    Generic test function to check single json at a time
    """
    json_response = get_json(response)

    request.node.add_marker(pytest.mark.test_type(test["type"]))

    if test["type"] == "timeout":
        logger.info(f"Testing timeout for {response.url}")
        expected_timeout = test["value"] or test_runner.config.default_test_settings['timeout_seconds']
        if expected_timeout:
            request.node.add_marker(pytest.mark.expected(str(expected_timeout)))  # Replace with actual expected value logic
            request.node.add_marker(pytest.mark.actual(str(response.elapsed.total_seconds())))                 
            assert (
                response.elapsed.total_seconds() <= expected_timeout
            ), f"Expected timeout: {expected_timeout}, Actual timeout: {response.elapsed.total_seconds()} Response: {json_response}"

    if test["type"] == "statusCode":
        logger.info(f"Testing status code for {response.url} ")
        expected_status_code = test["value"] or test_runner.config.default_test_settings['expected_status_code']
        if expected_status_code:
            request.node.add_marker(pytest.mark.expected(str(expected_status_code)))
            request.node.add_marker(pytest.mark.actual(str(response.status_code)))                 
            assert (
                response.status_code == expected_status_code
            ), f"Expected status code: {expected_status_code}, Actual status code: {response.status_code} Response: {json_response}"
    
    if test["type"] == "jsonSchema":
        logger.info(f"Testing json schema for {response.url} ")
        if isinstance(test["value"], str):
            class_name = test["value"]
            class_ = get_class(class_name, "rest_tester.tests.responses")
        expected_json_schema = class_.model_json_schema() if class_ else test["value"]
        if expected_json_schema and json_response:
            request.node.add_marker(pytest.mark.expected(json.dumps(expected_json_schema)))
            try:
                jsonschema.validate(json_response, expected_json_schema)
                request.node.add_marker(pytest.mark.actual(json.dumps(expected_json_schema)))
            except jsonschema.exceptions.ValidationError as e:
                request.node.add_marker(pytest.mark.actual(json.dumps(get_json_schema(json_response, class_name))))
                pytest.fail(f"JSON Schema validation failed: {str(e)}\n Response: {json_response}")
