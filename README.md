# python-rest-tester-framework
Welcome to the Python REST tester, the API Testing Framework, with a robust and flexible solution for testing REST-based applications. This framework is built on the powerful Pytest library and is designed to work with Python 3.10, ensuring you have the latest features at your disposal.

## Features
  **Comprehensive HTTP Method Support**: Whether you're testing GET, POST, PUT, DELETE, or any other HTTP method, our framework has you covered.
  
  **Authentication and Custom Headers**: Easily configure authentication and add custom headers to your requests to test secured endpoints.
  
  **Dockerized Setup**: Get up and running quickly with our Dockerized environment, ensuring consistency across different systems.
  
  **Sample Tests with Public APIs**: Jumpstart your testing with our sample tests that utilize public APIs, giving you a practical reference point.
  
  **Configuration Management**: Manage your test configurations with ease using our configs.py file and support for environment variables.
  
  **Modular and Extensible**: Our class-based code structure allows for easy extension and customization to fit your unique testing needs.
  
  **Pydantic Data Models**: Replace repetitive JSON schemas with named Pydantic classes for a more efficient and maintainable test data setup.
  
  **Makefile for Convenience**: Utilize our Makefile for straightforward command execution and streamline your testing workflow.

  **Compatible with Openapi spec and Postman collection**: Utilize your exsisting postman collection JSON or Openapi collection JSON/YAML to fasten the test suite creation as boiler plate for your convenience.

  **Automatic sample params and payload generation**: The 'jsf' module is used for this, which is made on top of the powerful 'Faker' module and currenlty implemented in openapi specification parsing.

## Utilities
---
1. You can also use the parser as a utility by providing the openapi spec/postman collection file path as input argument.
	```sh
	$ python3 <root_path>/postman_parser.py <path_to_postman_collection>
	```
	or
	```sh
	$ python3 <root_path>/openapi_parser.py <path_to_openapi_spec>
	```
---

## To get token for Public API:  
---
1. Send a POST request to 'https://dummyjson.com/auth/login' with below JSON body,
	```json
	{
    "username": "emilys",
    "password": "emilyspass",
    "expiresInMins": 30, // optional, defaults to 60
  	}
	```
2. You can use any user's credentials from 'dummyjson.com/users'.
---

## To install the application via docker:
---
1. Execute the following commands to get started:,
	```sh
	$ git clone https://github.com/BigThinkcode/python-rest-tester
    $ cd python-rest-tester
	```
2. To run the app straight away with HTML report after setting up tests and configs in dev mode, use below make command,
	```sh
	$ make run-dev
	```
3. To build and start interactive shell to use the application in dev, use below make command,
	```sh
	$ make run-dev-shell
	```
	NOTE: This method has limitation that you have to place your test groups directory inside the 'rest_tester/' only, not outside of it.
---

## To install the application via virtual environment:
---
1. Execute the following commands to get started:,
	```sh
	$ git clone https://github.com/BigThinkcode/python-rest-tester
    $ cd python-rest-tester
	```
2. Create a virtual environment using below command,
	```sh
	$ python3 -m venv <name of the virtual environment>
	```
3. Activate the virtual environment using,
	```sh
	$ source <name of the virtual environment>/bin/activate
	```
4. Install poetry and then all dependencies using,
	```sh
	$ pip install --no-cache-dir poetry==1.4.2; poetry install
	```
---

## To run the application:
---
1. After installation by any of the above method, run below command to see available commands to use under 'app' section,
	```sh
	$ make help
	```
2. If you run 'make test', default public apis will be tested.

3. Place the test groups somewhere inside the 'rest_tester/' directory and set the directory path in the configuration file under 'execution_settings'.If using virtual environment, then you can place them anywhere you want.

4. If any test group need authentication, set 'token' under 'users' section.

5. If token cannot be decoded, then you can specify token_validation endpoint under 'token_validation' in 'auth_settings'.

6. Once the above steps are completed, you can run the tests by using the following command:
	```sh
	$ make test
	```
7. If you want to run your tests along with report generation, you can use the below command:
	```sh
	$ make test-with-report
	```
---

# Testing Configuration Guide

This document serves as a guide for configuring test settings for API testing.

## Overview

The provided `configs` dictionary contains various settings that define how API tests should be executed. These settings include default test expectations, request-related settings, authentication configurations, user accounts for testing, and execution settings.

## Configuration Sections

### Test Defaults

These settings define the standard expectations for the API tests and are taken into account if a test json doesn't have these settings:

- `expected_status_code`: The HTTP status code that API responses should return by default.
- `timeout_seconds`: The maximum time in seconds to wait for a response before considering the test as failed due to a timeout.

### HTTP Request Settings

Settings related to the construction and sending of HTTP requests:

- `request_method`: Type of request method, options include "basic" or "session" for HTTP session-based requests as shown in `allowed_methods`.
- `base_url`: The base URL for the API endpoints to be tested.
- `verify_ssl`: A boolean that determines whether SSL certificates need to be verified or not.

### Authentication Settings

Configurations for managing and using authentication tokens in API tests:

- `token_encoded`: A boolean that indicates whether the token is encoded.
- `encoding_format`: The encoding format of the token; this is `None` if `token_encoded` is `False`.
- `auth_headers`: A list of dictionaries representing headers that need to be added to each API request, with support for token placeholders.
- `token_validation`: The API endpoint settings used to verify if the token is still valid.

### User Tokens

A list of user profiles available for testing:

- Each user has a `token` and a list of `test_groups` associated with them, no `token` needed for non-authentication groups.
- `test_groups` identify the groups for which tests to be executed for the user.

### Execution Settings

Settings that determine how tests should be executed and how logs should be captured:

- `log_level`: The verbosity level of the logs, typically set to "DEBUG" for comprehensive logging.
- `log_format`: The format of log messages; represented by a number correlating to a specific format.
- `dir_groups_to_test`: Basically this is the local file path where test group definitions are stored, you can also define the path of JSON/YAML of openapi collection or JSON of postman collection.
- `auto_convert`: A boolean that indicates that whether to convert the openapi spec JSON/YAML or postman collection JSON specified in `dir_groups_to_test` directly or not. Setting this to `False` is recommended as most of the time manual intervention needed after conversion.

## Using Configurations

When writing tests:

1. Update `user_tokens` with appropriate tokens and test groups as required for the application being tested.
2. Ensure `http_request_settings` matches the API's request method and SSL requirements.
3. Customize `authentication_settings` to include all necessary headers. The provided placeholder `{token}` in `auth_headers` will be replaced with the actual token value during the test run.
4. Modify `default_test_settings` to reflect the expected status code and timeout values for the API endpoints.
5. Set `execution_settings` based on your logging preferences and where test groups are located.

### API Testing Configuration
To perform API testing, please specify the details of your API and the testing parameters.

## API Configuration
In the api section, provide the following information:

**URI**: Set the target REST API URI by specifying the uri.
**Method**: Define the HTTP request method using the method field.
**Parameters**: If applicable, you can set the parameters using the params field.
## Test Configuration
In the tests section, include the following test case details:

**Timeout**: Specify the timeout period for receiving the API response (in seconds) using the timeout field.
**Status Code**: Define the expected HTTP status code using the statusCode field.
**JSON Schema**: Specify the JSON Schema that the response should satisfy. You can use the JSON Schema notation and provide it in the jsonSchema field.
If you are familiar with pydantic, it is recommended to represent repetitive parts of your test JSON as pydantic data models.

Here's an example configuration that demonstrates a GET API call to http://0.0.0.0:8005/. It includes the corresponding test checks:

```json
	{
		"api": {
		"uri": "http://0.0.0.0:8005/",
		"method": "get"
		},
	
		"tests": {
		"timeout" : 10,
		"statusCode": 200,
		"jsonSchema": {
		    "type": "object",
		    "properties": {
			"message": {
			    "type": "string"
			}
		    }    
		}
	    }
	}
```

You can find sample json and pydantic models inside the **tests** folder

### Pydantic Data Model Generation
To generate a Pydantic data model for an API response in the rest_tester directory, follow these steps:

Inside the data_model_codegen directory, locate the empty JSON file named your_response_or_payload.json.
Copy and paste the actual response from the API as a JSON object into this file.
Run the following command, replacing the necessary placeholders with your own values:

```sh
$ datamodel-codegen --input /<your_root_path>/python-api-testing-framework/rest_tester/data_model_codegen/response_json.json --input-file-type json --output /<your_root_path>/python-api-testing-framework/rest_tester/data_model_codegen/response_or_data_model.py --output-model-type pydantic_v2.BaseModel --class-name <Name as per needed>
```
Note: You can customize the paths and input types as per your requirements.

For example, if the sample JSON schema is as follows:

```json
"jsonSchema": {
	        "type": "object",
	        "properties": {
		"message": {
		    "type": "string"
		    }
	         }    
              }
``` 

The generated Pydantic model code will be:
```
class Message(BaseModel):
    Message: str
```

Please keep in mind that the autogenerated code serves as a starting point and should be reviewed and modified as needed, as it may not generate perfectly optimized code like a human with Pydantic knowledge.


### Makefile
---
The Makefile serves as the "entrypoint" for the tools within this structure, allowing you to conveniently execute various commands without needing to recall the specific arguments. To view a list of available commands, you can run make help. This will provide you with an overview of the commands at your disposal.
```sh
$ make help
Available commands:
[For docker related]
  local-remove-images        Removes locally present dangling images
  run-dev-shell              Run the application in Dev mode once build completed as interactive shell
  run-dev                    Run the application in Dev mode once build completed
  run-prod                   Run the application in Prod mode once build completed
[For app related]
  check-lint                 Check Lint
  lint                       Lint
  test                       To performs all tests
  test-with-report           To performs all tests and generate a HTML report file
```
Make allows you to collect common scripts and commands for the project.
Other projects using different programming languages and frameworks get the same development interface by using Make.

---

## Road Map:

+ Multiple types of report generation​

+ Support for concurrency and asynchronous requests​

+ Improve HTML report visualisation​

+ Support for automatic trigger for git commit or merge​

+ Support for triggering via API call​

+ UI for ease of use

+ Chained api testing - mimic user flow

+ Chain multiple tests  - individual test will have its own result

+ UI testing

+ Support for WS, GraphQL etc

+ n times hitting, other testing facilites like mock user traffic

## Questions?

If you have any questions regarding the setting up the app or testing, please feel free to open an issue in the repository.