# hyperproof/roles_api.py
from .utils import APIClient

class RolesAPI:
    """
    This class handles interactions with the Roles API of Hyperproof.
    It allows retrieving a list of roles in the organization.
    """
    BASE_URL = "https://api.hyperproof.app/v1/roles"

    def __init__(self, client_id, client_secret):
        # Initialize the API client with authentication
        self.client = APIClient(client_id, client_secret)

    def get_roles(self, raw=False):
        """
        Retrieves a list of roles in the organization.

        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        return self.client.get(self.BASE_URL, "/", raw=raw)
