import requests
import logging
from requests.exceptions import HTTPError, RequestException, Timeout, ConnectionError

logger = logging.getLogger('GRC_Agent')

TOKEN_ENDPOINT = "https://accounts.hyperproof.app/oauth/token"

class APIClient:
    """
    This class handles the authentication and token management using OAuth 2.0.
    It is responsible for sending HTTP requests (GET, POST, PATCH) to Hyperproof's API.
    """

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None

        # Attempt to get an access token on initialization
        try:
            self._authenticate()
        except Exception as e:
            logger.error(f"Failed to authenticate: {e}")
            self.access_token = None

    def _authenticate(self):
        """
        Authenticates using client credentials to obtain an OAuth 2.0 access token.
        """
        logger.debug("Authenticating to get access token")
        params = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        try:
            response = requests.post(TOKEN_ENDPOINT, data=params)
            logger.debug(f"Token request status code: {response.status_code}")

            if response.status_code == 200:
                response_json = self._parse_json(response)
                self.access_token = response_json.get('access_token')
                logger.debug("Access token retrieved successfully")
            else:
                logger.error(f"Failed to retrieve access token: {response.status_code} {response.text}")
                self.access_token = None

        except (HTTPError, ConnectionError, Timeout, RequestException) as err:
            logger.error(f"Error during authentication: {err}")
            self.access_token = None

    def _get_headers(self):
        """
        Generates headers for API requests, including the Bearer token.
        """
        if not self.access_token:
            logger.debug("Access token not found. Re-authenticating...")
            self._authenticate()

        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    def get(self, base_url, endpoint, params=None, raw=False):
        """
        Sends a GET request to the API.

        :param base_url: The base URL for the API (specific to the API being used).
        :param endpoint: The specific endpoint (path) to call.
        :param params: Query parameters to include in the request.
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format.
        """
        try:
            response = requests.get(f"{base_url}{endpoint}", headers=self._get_headers(), params=params)
            return self._handle_response(response, raw=raw)
        except Exception as e:
            logger.error(f"GET request failed: {e}")
            return None

    def post(self, base_url, endpoint, data=None, files=None, raw=False):
        """
        Sends a POST request to the API.

        :param base_url: The base URL for the API (specific to the API being used).
        :param endpoint: The specific endpoint (path) to call.
        :param data: JSON body to send with the request (if applicable).
        :param files: Files to upload (if applicable).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format.
        """
        try:
            if files:
                response = requests.post(f"{base_url}{endpoint}", headers=self._get_headers(), files=files)
            else:
                response = requests.post(f"{base_url}{endpoint}", headers=self._get_headers(), json=data)
            return self._handle_response(response, raw=raw)
        except Exception as e:
            logger.error(f"POST request failed: {e}")
            return None

    def patch(self, base_url, endpoint, data=None, raw=False):
        """
        Sends a PATCH request to the API.

        :param base_url: The base URL for the API (specific to the API being used).
        :param endpoint: The specific endpoint (path) to call.
        :param data: JSON body to send with the request.
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format.
        """
        try:
            response = requests.patch(f"{base_url}{endpoint}", headers=self._get_headers(), json=data)
            return self._handle_response(response, raw=raw)
        except Exception as e:
            logger.error(f"PATCH request failed: {e}")
            return None

    def _handle_response(self, response, raw=False):
        """
        Handles the HTTP response, checking for success or failure.

        :param response: The HTTP response from the API.
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response in the desired format, or None if an error occurs.
        """
        try:
            # Raise an error for non-200 status codes
            response.raise_for_status()

            # Return raw response if requested
            if raw:
                return response.text

            # Parse JSON response
            return self._parse_json(response)

        except HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err} - {response.text}")
            return None
        except ValueError as val_err:
            logger.error(f"JSON decoding error: {val_err}")
            return None
        except Exception as err:
            logger.error(f"An error occurred when handling the response: {err}")
            return None

    def _parse_json(self, response):
        """
        Safely parses the JSON from the response. Logs an error if the content type isn't JSON.
        
        :param response: The HTTP response object.
        :return: Parsed JSON data or an empty dict if parsing fails.
        """
        try:
            if 'application/json' in response.headers.get('Content-Type', ''):
                return response.json()
            else:
                logger.error(f"Unexpected content type: {response.headers.get('Content-Type')}")
                return {}
        except ValueError as val_err:
            logger.error(f"Error parsing JSON: {val_err}")
            return {}
