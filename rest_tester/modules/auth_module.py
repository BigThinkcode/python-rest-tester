"""
This file has Authenticator class and its properties
"""

import datetime
import base64, binascii
import json,re

from rest_tester.logger import logger

class Authenticator:
    """
    This class is responsible for handling Authentication related functions.
    """

    def __init__(self, authentication_configs: dict, api_client):
        """
        Initialize the Authenticator object with user login settings, authentication configurations, and api client.

        Parameters:
            user_login_settings (dict): The settings related to user login.
            authentication_configs (dict): The configurations related to authentication.
            api_client: The api client for handling requests.
        """
        self.authentication_configs = authentication_configs
        self.api_client = api_client

    @staticmethod
    def safe_format(template, **kwargs):
        """
        Safely formats a template string by replacing placeholders with provided keyword arguments.

        Parameters:
            template (str): The template string to be formatted.
            **kwargs: Keyword arguments containing the values to replace the placeholders in the template.

        Returns:
            str: The formatted template string with placeholders replaced by the corresponding keyword arguments.

        Example:
            >>> safe_format("Hello, {name}!", name="Alice")
            'Hello, Alice!'
        """
        for key in kwargs:
            if '{' + key + '}' in template:
                template = template.replace('{' + key + '}', kwargs[key])
        return template

    def login(self, token: str) -> None:
        """
        This method iterates over the 'auth_headers' list in the authentication configurations and formats each header by replacing placeholders with values from the user login settings. The formatted headers are then added to the api client's headers.

        Parameters:
            self (Authenticator): The instance of the Authenticator class.
            token (str): The token needed to perform login action

        Returns:
            None
        """
        if token:
            for header_template in self.authentication_configs['auth_headers']:
                formatted_headers = {header: self.safe_format(value, **{'token': token}) for header, value in header_template.items()}
                self.api_client.headers.update(formatted_headers)

    def logout(self):
        """
        Logs out the user from the current session.

        Parameters:
            self (Authenticator): The instance of the Authenticator class.

        Returns:
            None
        """
        pass
        
    def is_token_valid(self, token: str) -> None:
        """
        Checks if the token is valid.

        This function checks if the token provided in the user login settings is valid.

        Parameters:
            self (Authenticator): The Authenticator instance.
            token (str): The token to be checked

        Returns:
            None

        Raises:
            Exception: If the provided token has expired.

        """
        if token:
            if self.authentication_configs.get('token_encoded', ''):
                token = self.decode_token(self.authentication_configs.get('encoding_format', ''), token)
                token_expiry_time = datetime.datetime.fromtimestamp(token['exp'])
                if datetime.datetime.now() < token_expiry_time:
                    return
            else:
                token_validation_params = self.authentication_configs['token_validation_params']
                settings = {
                            "params": token_validation_params.get('params', {}),
                            "json": token_validation_params.get('data', {}),
                            }
                response = self.api_client.send_request(token_validation_params['method'], token_validation_params['uri'], **settings)
                if response.status_code == 200:
                    return
            raise Exception('Provided token expired, add new token and restart test...')

    def decode_token(self, type: str, token: str) -> dict:
        """
        Decode the provided token based on the specified encoding type.

        Args:
            type (str): The encoding type of the token. Currently, only 'base64' is supported.
            token (str): The token to be decoded

        Returns:
            dict: The decoded token payload as a dictionary.
        """
        try:
            if type == 'base64':
                logger.info(f"Decoding token: {token}")
                payload_raw = base64.urlsafe_b64decode(token+'==')
                payload_json = re.findall(r"{.*?}", str(payload_raw))[1]
                return json.loads(payload_json)
        except (IndexError, json.JSONDecodeError, binascii.Error) as error:
            logger.info(f"Error decoding token: {error}")