"""
This file contains functions for converting postman collection to folder structure
"""

import os
import re
import json
import sys
from rest_tester.logger import logger
from postmanparser import Collection

def remove_placeholders(uri: str) -> str:
    """
    Removes placeholders from the given URI.

    Args:
        uri (str): The URI from which to remove placeholders.

    Returns:
        str: The URI with placeholders removed.
    """
    return re.sub(r'\{\{[^}]+\}\}', '', uri)

def extract_query_params(request: Collection) -> list:
    """
    Extracts query parameters from the given request object and returns a list of dictionaries containing the key-value pairs of the parameters.
    
    Args:
        request: The request object containing the URL query parameters.
    
    Returns:
        list: A list of dictionaries representing the extracted query parameters.
    """
    params = []
    if request.url.query:
        for param in request.url.query:
            params.append({
                param.key: param.value
            })
    return params

def extract_body_data(request: Collection) -> list|str:
    """
    Extracts the body data from a request object.

    Args:
        request (Request): The request object.

    Returns:
        list or str: The extracted body data.
    """
    data = []
    if request.body and request.body.mode == 'raw':
        try:
            data = json.loads(request.body.raw)
        except json.JSONDecodeError:
            data = request.body.raw
    return data

def create_dir_and_json(item: Collection, parent_dir: str) -> None:
    """
    Creates a directory and a JSON file containing API details for each sub-item in the given item.
    
    Args:
        item (object): The item containing sub-items.
        parent_dir (str): The parent directory where the group directory will be created.
    
    Returns:
        None
    """
    group_dir = os.path.join(parent_dir, item.name.replace(' ', '_'))
    os.makedirs(group_dir, exist_ok=True)
    
    api_details = []
    
    for sub_item in item.item:
        uri = remove_placeholders(sub_item.request.url.raw)
        params = extract_query_params(sub_item.request)
        data = extract_body_data(sub_item.request)
        api_detail = {
            "api": {
                "uri": uri,
                "method": sub_item.request.method.lower(),
                "param": params,
                "data": data
            },
            "tests": {
                "statusCode": 200,
                "timeout": 10
            }
        }
        api_details.append(api_detail)
    
    with open(os.path.join(group_dir, 'tests.json'), 'w') as json_file:
        json.dump(api_details, json_file, indent=4)

def convert_from_postman(test_groups_path: str) -> str:
    """
    Converts a Postman collection to a directory structure containing API details.
    
    Args:
        test_groups_path (str): The path to the Postman collection file.
    
    Returns:
        str: The root directory where the converted collection is stored.
    """
    collection_path = test_groups_path
    collection = Collection()
    collection.parse_from_file(collection_path)

    root_dir = os.path.dirname(collection_path)
    root_dir += collection.info.name.replace(' ', '_')
    os.makedirs(root_dir, exist_ok=True)

    for item in collection.item:
        if item.item:
            create_dir_and_json(item, root_dir)
        else:
            logger.info('\nNo requests in this group')

    logger.info(f"Collection '{collection.info.name}' has been processed.")

    return root_dir

if __name__ == "__main__":
    if sys.argv[1]:
        print(f"Result: {convert_from_postman(sys.argv[1])}")
    else:
        print("Usage: python3 postman_parser.py <path_to_postman_collection>")