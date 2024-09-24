# hyperproof/risks_api.py
from .utils import APIClient

class RisksAPI:
    """
    This class handles interactions with the Risks API of Hyperproof.
    It allows retrieving, adding, filtering, and updating risks in an organization.
    """
    BASE_URL = "https://api.hyperproof.app/v1/risks"

    def __init__(self, client_id, client_secret):
        # Initialize the API client with authentication
        self.client = APIClient(client_id, client_secret)

    def get_risks(self, risk_register_id=None, status=None, raw=False):
        """
        Retrieves all risks for the organization with optional filters by risk register or status.

        :param risk_register_id: The unique ID of the risk register (optional).
        :param status: Filter by the status of the risks (optional, e.g., 'active', 'archived').
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        params = {
            'riskRegisterId': risk_register_id,
            'status': status
        }
        return self.client.get(self.BASE_URL, "/", params=params, raw=raw)

    def add_risk(self, risk_register_id, risk_identifier, name, description, category, response,
                 likelihood_level, likelihood_rationale, impact_level, impact_rationale,
                 tolerance_level, owner_id, raw=False):
        """
        Adds a new risk to an organization.

        :param risk_register_id: The unique ID of the risk register.
        :param risk_identifier: The identifier for the risk.
        :param name: Name of the risk.
        :param description: Description of the risk.
        :param category: Category of the risk.
        :param response: Risk response strategy (e.g., 'mitigate', 'accept').
        :param likelihood_level: Likelihood level (e.g., 1-5).
        :param likelihood_rationale: Explanation for the likelihood level.
        :param impact_level: Impact level (e.g., 1-5).
        :param impact_rationale: Explanation for the impact level.
        :param tolerance_level: Tolerance level for the risk.
        :param owner_id: The owner ID for the risk.
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        data = {
            "riskRegisterId": risk_register_id,
            "riskIdentifier": risk_identifier,
            "name": name,
            "description": description,
            "category": category,
            "response": response,
            "likelihoodLevel": likelihood_level,
            "likelihoodRationale": likelihood_rationale,
            "impactLevel": impact_level,
            "impactRationale": impact_rationale,
            "toleranceLevel": tolerance_level,
            "ownerId": owner_id
        }
        return self.client.post(self.BASE_URL, "/", data=data, raw=raw)

    def get_risk_by_id(self, risk_id, raw=False):
        """
        Retrieves a specific risk by its unique ID.

        :param risk_id: The unique ID of the risk.
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        return self.client.get(self.BASE_URL, f"/{risk_id}", raw=raw)

    def update_risk(self, risk_id, name=None, description=None, category=None, response=None,
                    likelihood_level=None, likelihood_rationale=None, impact_level=None,
                    impact_rationale=None, tolerance_level=None, status=None, owner_id=None, raw=False):
        """
        Updates an existing risk with new values.

        :param risk_id: The unique ID of the risk.
        :param name: Updated name of the risk (optional).
        :param description: Updated description of the risk (optional).
        :param category: Updated category of the risk (optional).
        :param response: Updated risk response strategy (optional).
        :param likelihood_level: Updated likelihood level (optional).
        :param likelihood_rationale: Updated explanation for likelihood level (optional).
        :param impact_level: Updated impact level (optional).
        :param impact_rationale: Updated explanation for impact level (optional).
        :param tolerance_level: Updated tolerance level (optional).
        :param status: Updated status of the risk (optional, e.g., 'active', 'archived').
        :param owner_id: Updated owner ID for the risk (optional).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        data = {
            "name": name,
            "description": description,
            "category": category,
            "response": response,
            "likelihoodLevel": likelihood_level,
            "likelihoodRationale": likelihood_rationale,
            "impactLevel": impact_level,
            "impactRationale": impact_rationale,
            "toleranceLevel": tolerance_level,
            "status": status,
            "ownerId": owner_id
        }
        return self.client.patch(self.BASE_URL, f"/{risk_id}", data=data, raw=raw)

    def filter_risks(self, risk_ids=None, modified_after=None, status=None, raw=False):
        """
        Filters risks based on a set of criteria like risk IDs, modification date, and status.

        :param risk_ids: List of risk IDs to filter by (optional).
        :param modified_after: Only return risks modified after this date (optional).
        :param status: Filter by risk status (optional).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        data = {
            "riskIds": risk_ids or [],
            "modifiedAfter": modified_after,
            "status": status
        }
        return self.client.put(self.BASE_URL, "/filter", data=data, raw=raw)
