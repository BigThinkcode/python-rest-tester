"""
This file contains the configurations using which testing performed
"""

configs = {   
    "default_test_settings": {
        # Default expected HTTP status code for successful requests
        "expected_status_code": 200,
        # Timeout in seconds for each request
        "timeout_seconds": 10
    },
    "http_request_settings": {
        # Method to use for making requests (e.g., "basic" for simple requests, "session" for persistent sessions)
        "method": "session",
        # Base URL for the API under test
        "base_url": "https://dummyjson.com",
        # Whether to verify SSL certificates for HTTPS requests
        "verify_ssl": True,
        # List of allowed methods for making requests
        "allowed_methods": ["basic", "session"]
    },
    "auth_settings": {
        # Indicates if the token is encoded
        "token_encoded": True,
        # Format for encoding the token (e.g., "base64", "jwt"), if applicable
        "encoding_format": "base64",
        # Headers to add to requests for authentication, with placeholders for token substitution
        "auth_headers": [{"Authorization": "Bearer {token}"}],
        # Configuration for validating the token, including method, URI, and parameters
        "token_validation_params": {
            "method": 'get',
            "uri": '/user/me'
        }
    },
    "user_tokens": [
        # List of users, each with associated tokens and test groups
        {
            # List of test groups for the user (e.g., paths to test cases)
            "test_groups": ["group1/"]
        },
        {
            # Token for the user
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJlbWlseXMiLCJlbWFpbCI6ImVtaWx5LmpvaG5zb25AeC5kdW1teWpzb24uY29tIiwiZmlyc3ROYW1lIjoiRW1pbHkiLCJsYXN0TmFtZSI6IkpvaG5zb24iLCJnZW5kZXIiOiJmZW1hbGUiLCJpbWFnZSI6Imh0dHBzOi8vZHVtbXlqc29uLmNvbS9pY29uL2VtaWx5cy8xMjgiLCJpYXQiOjE3MjAxMzE1NTUsImV4cCI6MTcyMDEzNTE1NX0.UeOhe-VgV8ojCgPgV8mqlJne18fubOuziPMRJxjkf8A",
            # List of test groups for the user
            "test_groups": ["group2/"]
        },
        {
            # Token for the user
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NCwidXNlcm5hbWUiOiJqYW1lc2QiLCJlbWFpbCI6ImphbWVzLmRhdmlzQHguZHVtbXlqc29uLmNvbSIsImZpcnN0TmFtZSI6IkphbWVzIiwibGFzdE5hbWUiOiJEYXZpcyIsImdlbmRlciI6Im1hbGUiLCJpbWFnZSI6Imh0dHBzOi8vZHVtbXlqc29uLmNvbS9pY29uL2phbWVzZC8xMjgiLCJpYXQiOjE3MjAxMzE1NzksImV4cCI6MTcyMDEzNTE3OX0.QL7GISIhcyYg8hEAb7rGTsp3FcELnWrhFgvp9XuO8dQ",
            # List of test groups for the user
            "test_groups": ["group3/"]
        }
    ],
    "execution_settings": {
        # Log level for test execution (e.g., "DEBUG", "INFO", "ERROR")
        "log_level": "DEBUG",
        # Log format to use for logging output
        "log_format": "3",
        # Directory path where test groups are located
        "dir_groups_to_test": "/app/rest_tester/tests/public_api/",
        # Whether to directly convert and use Openapi spec file if given
        "auto_convert": False
    }
}