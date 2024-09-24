# hyperproof/controls_api.py
from .utils import APIClient

class ControlsAPI:
    """
    This class handles interactions with the Controls API of Hyperproof.
    """
    BASE_URL = "https://api.hyperproof.app/v1/controls"

    def __init__(self, client_id, client_secret):
        # Initialize the API client with authentication
        self.client = APIClient(client_id, client_secret)

    def get_controls(self, can_link=None, expand_scopes=None, expand_teams=None, status=None, raw=False):
        """
        Retrieve all controls for the organization with optional filters.

        :param can_link: Filter by link permission (optional).
        :param expand_scopes: Whether to expand scopes (optional).
        :param expand_teams: Whether to expand teams (optional).
        :param status: Filter by control status (optional).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format.
        """
        params = {
            'canLink': can_link,
            'expandScopes': expand_scopes,
            'expandTeams': expand_teams,
            'status': status
        }
        return self.client.get(self.BASE_URL, "/", params=params, raw=raw)

    def get_control_by_id(self, control_id, raw=False):
        """
        Retrieve a specific control by its unique ID.

        :param control_id: The ID of the control to retrieve.
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: JSON response of the control.
        """
        return self.client.get(self.BASE_URL, f"/{control_id}", raw=raw)

    def add_control(self, control_identifier, name, description, domain_name, owner, implementation="inProgress"):
        """
        Add a new control to the organization.

        :param control_identifier: The identifier for the control.
        :param name: Name of the control.
        :param description: Description of the control.
        :param domain_name: Domain under which the control falls.
        :param owner: Owner of the control.
        :param implementation: Implementation status (default is inProgress).
        :return: JSON response of the newly added control.
        """
        data = {
            "controlIdentifier": control_identifier,
            "name": name,
            "description": description,
            "domainName": domain_name,
            "implementation": implementation,
            "owner": owner
        }
        return self.client.post(self.BASE_URL, "/", data)
