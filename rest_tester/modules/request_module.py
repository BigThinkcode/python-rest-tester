"""
This file has the RequestSender class with its methods
"""

import requests
from rest_tester.logger import logger
 
class APIClient:
    """
    This class handles HTTP requests using the requests library and configurations provided.
    """
 
    def __init__(self, config):
        """
        Initialize the APIClient with configurations.
 
        Args:
            config (dict): Configuration dictionary containing 'base_url', 'verify_ssl', and optional 'headers'.
        """
        self.session = requests.Session()
        self.base_url = config.base_url
        self.verify_ssl = config.verify_ssl
        self.headers = {}
 
    def send_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Send an HTTP request.
 
        Args:
            method (str): HTTP method (e.g., 'GET', 'POST').
            endpoint (str): API endpoint to send the request to.
            **kwargs: Additional arguments to pass to the requests method.
 
        Returns:
            requests.Response: The HTTP response object.
        """
        url = self.base_url + endpoint
        try:
            logger.info(f'Sending {method} request to {url} with headers {self.headers} and params {kwargs}')
            with requests.request(method, url, verify=self.verify_ssl, headers=self.headers, **kwargs) as response:
                logger.info(f'Received response: {response.status_code} for {url}')
                return response
        except requests.exceptions.RequestException as e:
            logger.error(f'Error occurred during request to {url}: {e}')
            raise
 
class SessionAPIClient(APIClient):
    """
    This class handles HTTP requests using a persistent session.
    """
 
    def send_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Send an HTTP request using a session.
 
        Args:
            method (str): HTTP method (e.g., 'GET', 'POST').
            endpoint (str): API endpoint to send the request to.
            **kwargs: Additional arguments to pass to the requests method.
 
        Returns:
            requests.Response: The HTTP response object.
        """
        url = self.base_url + endpoint
        try:
            logger.info(f'Sending {method} request to {url} with headers {self.headers} and params {kwargs}')
            with self.session.request(method, url, verify=self.verify_ssl, headers=self.headers, **kwargs) as response:
                logger.info(f'Received response: {response.status_code} for {url}')
                return response
        except requests.exceptions.RequestException as e:
            logger.error(f'Error occurred during request to {url}: {e}')
            raise
 
def get_api_client(config):
    """
    Factory function to get the appropriate API client based on the configuration.
 
    Args:
        config (dict): Configuration dictionary containing 'request_method' and other settings.
 
    Returns:
        APIClient: An instance of the appropriate API client class.
    """
    api_clients = {
        'basic': APIClient,
        'session': SessionAPIClient,
    }
    api_client_class = api_clients.get(config.request_method)
    if not api_client_class:
        raise ValueError(f"Invalid request method: {config.request_method}")
    return api_client_class(config)
