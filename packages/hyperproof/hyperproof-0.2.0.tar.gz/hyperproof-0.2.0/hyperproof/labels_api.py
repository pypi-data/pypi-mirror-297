# hyperproof/labels_api.py
from .utils import APIClient

class LabelsAPI:
    """
    This class handles interactions with the Labels API of Hyperproof.
    """
    BASE_URL = "https://api.hyperproof.app/v1/labels"

    def __init__(self, client_id, client_secret):
        # Initialize the API client with authentication
        self.client = APIClient(client_id, client_secret)

    def get_labels(self, can_link=None, status=None, raw=False):
        """
        Retrieve all labels in the organization with optional filters.

        :param can_link: Filter by link permission (optional).
        :param status: Filter by label status (optional).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format.
        """
        params = {
            'canLink': can_link,
            'status': status
        }
        return self.client.get(self.BASE_URL, "/", params=params, raw=raw)

    def get_label_by_id(self, label_id, raw=False):
        """
        Retrieve a specific label by its unique ID.

        :param label_id: The ID of the label to retrieve.
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: JSON response of the label.
        """
        return self.client.get(self.BASE_URL, f"/{label_id}", raw=raw)

    def get_label_summaries(self, can_link=None, status=None, raw=False):
        """
        Retrieve label summaries for the organization with optional filters.

        :param can_link: Filter by link permission (optional).
        :param status: Filter label summaries by their status (optional).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format.
        """
        params = {
            'canLink': can_link,
            'status': status
        }
        return self.client.get(self.BASE_URL, "/summaries", params=params, raw=raw)

    def add_label(self, name, description, raw=False):
        """
        Add a new label to the organization.

        :param name: Name of the label.
        :param description: A brief description of the label.
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data of the newly added label.
        """
        data = {
            "name": name,
            "description": description
        }
        return self.client.post(self.BASE_URL, "/", data, raw=raw)

    def update_label(self, label_id, **kwargs):
        """
        Update an existing label with new values.

        :param label_id: The unique ID of the label to update.
        :param kwargs: Key-value pairs of the fields to update.
        :return: JSON response of the updated label.
        """
        return self.client.patch(self.BASE_URL, f"/{label_id}", kwargs)

    def add_label_proof(self, label_id, file_path, raw=False):
        """
        Add a proof item to a label.

        :param label_id: The unique ID of the label.
        :param file_path: Path to the file to upload as proof.
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data of the newly uploaded proof.
        """
        with open(file_path, 'rb') as file:
            files = {'file': file}
            return self.client.post(self.BASE_URL, f"/{label_id}/proof", files=files, raw=raw)
