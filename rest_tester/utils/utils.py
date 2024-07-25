"""
This file contains commonly used utility functions
"""

import json
import yaml
import requests

from rest_tester.logger import logger

def get_json(response: requests.Response) -> dict | None:
    """
    Method to process give response and return its JSON
    :param:
        response: Response for which need to be converted to JSON
    :returns:
        JSON format of the given response or none
    """
    try:
        json_response = response.json()
    except Exception as e:
        json_response = None
        logger.info(f"NON-JSON RESPONSE: {e}")
    return json_response

def get_class(class_name: str, module_path: str):
    """
    Returns desired class using its string representation
    :params:
        class_name: string represention of a class
        module_path: path where class present
    :returns:
        Class of the given string representation of the class.
    """
    logger.info(f"Fetching class {class_name} from {module_path}")
    import importlib

    module = importlib.import_module(module_path)
    class_ = getattr(module, class_name)
    logger.info(f"Successfully fetched class {class_name} from {module_path}")
    return class_

def read_json_file(filepath: str) -> list:
    """
    Method to read the json file from given path
    :param:
        filepath: Path where the json file located
    :returns:
        List of dictionaries read from given json file
    """
    with open(filepath, "r", encoding="utf-8") as json_file:
        try:
            jsons = json.load(json_file)
            logger.info(f"Successfully read: {filepath}")
        except json.JSONDecodeError as file_error:
            logger.info("Cannot parse the json file: %s" % str(file_error))
    return jsons

def get_json_schema(response_json, class_name='Response'):
    """
    Method to generate json schema for given json
    :param:
        response_json: Path where the json file located
        class_name: suitable class name for the response_json
    :returns:
        Json schema of the given json with given class name.
    """
    import importlib.util
    from pathlib import Path
    from tempfile import TemporaryDirectory
    from datamodel_code_generator import InputFileType, generate
    from datamodel_code_generator import DataModelType

    with TemporaryDirectory() as temporary_directory_name:
        temporary_directory = Path(temporary_directory_name)
        output = Path(temporary_directory / 'model.py')
        generate(
            json.dumps(response_json),
            input_file_type=InputFileType.Json,
            input_filename="example.json",
            output=output,
            output_model_type=DataModelType.PydanticV2BaseModel,
            class_name=class_name
        )
        spec = importlib.util.spec_from_file_location("model", output)
        generated_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generated_module)

        return getattr(generated_module, class_name).model_json_schema()
    