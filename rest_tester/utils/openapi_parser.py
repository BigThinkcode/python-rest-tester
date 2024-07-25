"""
This file contains functions for parsing OpenAPI specifications
"""

import os
import json
import yaml
import sys
from jsf import JSF
from rest_tester.logger import logger
from rest_tester.configs.constants import openapi_default_tag

def resolve_references(schema: dict, components: dict) -> dict:
    """
    Resolves references in a JSON schema by following the '$ref' keyword.

    Args:
        schema (dict): The JSON schema to resolve.
        components (dict): The components dictionary.

    Returns:
        dict: The resolved schema.
    """
    if isinstance(schema, dict) and "$ref" in schema:
        ref = schema["$ref"]
        ref_path = ref.split("/")[1:]  # Split the reference by '/'
        ref_schema = components['schemas']
        for key in ref_path:
            result_schema = ref_schema.get(key, None)
            if result_schema is None:
                continue
        if result_schema is None: 
            raise ValueError(f"Reference {ref} not found in components.")
        return result_schema
    elif isinstance(schema, dict) and "allOf" in schema:
        resolved = {"type": "object", "properties": {}, "required": []}
        for sub_schema in schema["allOf"]:
            sub_resolved = resolve_references(sub_schema, components)
            if sub_resolved:
                resolved["properties"].update(sub_resolved.get("properties", {}))
                resolved["required"] = list(set(resolved["required"] + sub_resolved.get("required", [])))
        resolved.update({k: v for k, v in schema.items() if k != "allOf"})
        return resolved
    elif isinstance(schema, dict):
        return schema
    else:
        return {}
    
def generate_sample_data(schema: dict) -> dict:
    """
    Generates sample data based on the given schema.

    Args:
        schema (dict): The schema to generate sample data from.

    Returns:
        dict: The generated sample data.
    """
    faker = JSF(schema)
    return faker.generate()
    
def generate_sample_data_for_payload(schema_name: str, components: dict) -> dict:
    """
    Generates sample data for a payload based on the given schema name and components.

    Args:
        schema_name (str): The name of the schema used to generate the payload.
        components (dict): The components dictionary containing the schema references.

    Returns:
        dict: The generated sample data for the payload.
    """
    resolved_schema = resolve_references(schema_name, components)
    return generate_sample_data(resolved_schema)

def generate_sample_data_for_param(param_schema: dict) -> dict:
    """
    A function that generates sample data for a parameter based on the parameter schema.

    Args:
        param_schema: The schema of the parameter for which sample data needs to be generated.

    Returns:
        The generated sample data based on the parameter schema.
    """
    return generate_sample_data(param_schema) 

def extract_params_schema(parameters: list) -> dict:
    """
    Extracts the schema information from a list of parameters and returns a JSON schema object.
    
    Args:
        parameters (list): A list of parameters containing schema information.
        
    Returns:
        dict: A JSON schema object representing the extracted properties and required fields.
    """
    properties = {}
    required = []
    
    for param in parameters:
        if 'schema' in param:
            properties[param['name']] = param['schema']
            if param.get('required', False):
                required.append(param['name'])
    
    json_schema = {
        "type": "object",
        "properties": properties
    }
    
    if required:
        json_schema["required"] = required
    
    return json_schema

def extract_request_body_schema(request_body: dict) -> dict:
    """
    Extracts the request body schema from the provided request body dictionary.

    Args:
        request_body (dict): The request body dictionary.

    Returns:
        dict: The schema of the request body if available, otherwise an empty dictionary.
    """
    content = request_body.get('content', {}).get('application/json', {})
    return content.get('schema', {})

def extract_responses_schema(responses: dict) -> dict:
    """
    Extracts the JSON schema from the 'responses' dictionary.

    Args:
        responses (dict): A dictionary containing the responses for different HTTP status codes.

    Returns:
        dict: The JSON schema extracted from the 'responses' dictionary. If the schema is not found, an empty dictionary is returned.
    """
    response_content = responses.get('200', {}).get('content', {}).get('application/json', {})
    return response_content.get('schema', {})

def create_dir_and_json(api_details: dict, tag: str, parent_dir: str) -> None:
    """
    Creates a directory based on the tag, and saves the provided API details in a JSON file within that directory.

    Args:
        api_details: The API details to be saved in the JSON file.
        tag: The tag used to create the directory name.
        parent_dir: The parent directory where the new directory will be created.

    Returns:
        None
    """
    tag_dir = tag.replace(' ', '_')
    full_dir = os.path.join(parent_dir, tag_dir)
    os.makedirs(full_dir, exist_ok=True)
    
    with open(os.path.join(full_dir, 'tests.json'), 'w') as json_file:
        json.dump(api_details, json_file, indent=4)

def convert_from_openapi(test_groups: str) -> str:
    """
    Converts an OpenAPI specification file to a set of API test groups.

    Args:
        test_groups (str): The path to the OpenAPI specification file.

    Returns:
        str: The root directory where the converted test groups are saved.
    """
    openapi_path = test_groups

    with open(openapi_path, 'r') as file:
        if openapi_path.endswith('.yaml'):
            openapi_spec = yaml.safe_load(file)
        elif openapi_path.endswith('.json'):
            openapi_spec = json.load(file)

    root_dir = os.path.dirname(openapi_path)
    root_dir += openapi_spec.get('info', {}).get('title', 'OpenAPI_Spec').replace(' ', '_')
    os.makedirs(root_dir, exist_ok=True)

    api_details_by_tag = {}
    components = openapi_spec.get('components', {})

    for path, methods in openapi_spec.get('paths', {}).items():
        for method, operation in methods.items():
            params_schema = extract_params_schema(operation.get('parameters', []))
            request_body_schema = extract_request_body_schema(operation.get('requestBody', {}))
            responses_schema = extract_responses_schema(operation.get('responses', {}))
            
            tag = operation.get('tags', [openapi_default_tag])[0]

            if params_schema:
                params_schema = generate_sample_data_for_param(params_schema)
            
            if request_body_schema:
                request_body_schema = generate_sample_data_for_payload(request_body_schema, components)

            if responses_schema:
                responses_schema = resolve_references(responses_schema, components)
            
            api_detail = {
                "api": {
                    "uri": path,
                    "method": method,
                    "param": params_schema,
                    "data": request_body_schema
                },
                "tests": {
                    "statusCode": 200,
                    "timeout": 10,
                    "jsonSchema": responses_schema
                }
            }
            
            if tag not in api_details_by_tag:
                api_details_by_tag[tag] = []
            api_details_by_tag[tag].append(api_detail)

    for tag, details in api_details_by_tag.items():
        create_dir_and_json(details, tag, root_dir)

    logger.info(f"OpenAPI specification '{openapi_spec.get('info', {}).get('title', 'OpenAPI_Spec')}' has been processed.")
    
    return root_dir

if __name__ == "__main__":
    if sys.argv[1]:
        print(f"Result: {convert_from_openapi(sys.argv[1])}")
    else:
        print("Usage: python3 openapi_parser.py <path_to_openapi_spec>")