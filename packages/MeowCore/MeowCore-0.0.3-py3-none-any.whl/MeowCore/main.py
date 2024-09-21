# iSHiKKi-Akabane - LilianPark

import requests
import logging

logger = logging.getLogger('MeowCore')
logger.setLevel(logging.DEBUG)


class MeowCore:
    """
    MeowCore 🐾 - A cat-tastic Python library that offers versatile utilities for developers.
    
    Attributes:
    -----------
    token : str
        The secret key (API token) to authenticate users.
    ai_key : str
        Stores the AI service key (None by default).
    scanner_key : str
        Stores the scanner service key (None by default).
    api_key : str
        Stores a general API key (None by default).
    meow_api : str
        The base URL for MeowCore API authentication.
    apiurl : str
        The Base URL for MeowCore API endpoints
    """

    def __init__(self, TOKEN: str):
        """
        Initialize MeowCore with the given API token. Automatically triggers 
        authentication with the MeowCore API to validate the provided token.

        :param TOKEN: The API token to authenticate and gain access to MeowCore services.
        :raises ValueError: If authentication fails due to invalid token.
        """
        self.token = TOKEN
        self.ai_key = None
        self.scanner_key = None
        self.api_key = None
        self.apiurl = None
        self.meow_api = "https://meow.api"
        self.authenticate()

    def authenticate(self):
        """
        Authenticate the user with the MeowCore API using the provided token.

        :raises ValueError: If the token is invalid or authentication fails.
        """
        if not self._validate_token():
            logger.error("Invalid API key provided for MeowCore 🐾. Access Denied! 😿")
            raise ValueError("Invalid API key provided for MeowCore.")
        
        logger.info("MeowCore loaded successfully!!! 🐾 Ready to purr and serve. 😸")

    def _validate_token(self):
        """
        Sends a POST request to the MeowCore API to validate the provided token.

        If authentication is successful, the response contains various keys like
        AI key, scanner key, and a general API key, which are stored for future use.

        :return: True if the token is valid and authentication is successful, False otherwise.
        :raises ConnectionError: If there is an issue connecting to the MeowCore API.
        :raises requests.RequestException: If an error occurs during the POST request.
        """
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(
                f"{self.meow_api}/auth", headers=headers
            )
            if response.status_code == 200:
                logger.info("Token validated successfully. You have purr-mission! 😺")
                key_data = response.json()["apikey"]
                self.ai_key = key_data["ai_key"]
                self.scanner_key = key_data["scanner_key"]
                self.api_key = key_data["api_key"]
                self.apiurl = response.json()["api_url"]
                return True
            else:
                logger.warning(f"Token validation failed! Status code: {response.status_code}. 😿")
                return False

        except requests.RequestException as e:
            logger.error(f"An error occurred during token validation: {e}. Looks like something went wrong! 😿")
            raise ConnectionError(f"Error connecting to {self.meow_api}")

        except Exception as e:
            logger.error(f"An error occurred during token validation: {e}. Looks like something went wrong! 😿")
            return False

