# hyperproof/proof_api.py
from .utils import APIClient

class ProofAPI:
    """
    This class handles interactions with the Proof API of Hyperproof.
    """
    BASE_URL = "https://api.hyperproof.app/v1/proof"

    def __init__(self, client_id, client_secret):
        # Initialize the API client with authentication
        self.client = APIClient(client_id, client_secret)

    def get_proof_metadata_collection(self, limit=25, sort_by="uploadedOn", sort_direction="desc", object_type=None, object_id=None, next_token=None, raw=False):
        """
        Retrieve the proof metadata for an organization, control, label, or task.

        :param limit: Maximum number of results to retrieve (default 25).
        :param sort_by: Field to sort results by (default is uploadedOn).
        :param sort_direction: Sort direction (asc or desc, default is desc).
        :param object_type: Filter by object type (control or label).
        :param object_id: Filter by object ID.
        :param next_token: Token for paginated results (optional).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format.
        """
        params = {
            'limit': limit,
            'sortBy': sort_by,
            'sortDirection': sort_direction,
            'objectType': object_type,
            'objectId': object_id,
            'nextToken': next_token
        }
        return self.client.get(self.BASE_URL, "/", params=params, raw=raw)

    def get_proof_metadata(self, proof_id, raw=False):
        """
        Retrieve specific proof metadata by proof ID.

        :param proof_id: The unique ID of the proof.
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data of the proof metadata.
        """
        return self.client.get(self.BASE_URL, f"/{proof_id}", raw=raw)

    def add_proof(self, file_path, object_id=None, object_type=None, raw=False):
        """
        Upload a new proof file to the organization.

        :param file_path: Path to the proof file to upload.
        :param object_id: The object ID the proof is related to (optional).
        :param object_type: The object type (control or label, optional).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data of the newly added proof.
        """
        with open(file_path, 'rb') as file:
            files = {'file': file}
            data = {}
            if object_id and object_type:
                data['objectId'] = object_id
                data['objectType'] = object_type
            return self.client.post(self.BASE_URL, "/", files=files, data=data, raw=raw)

    def add_proof_version(self, proof_id, file_path, raw=False):
        """
        Add a new version of an existing proof by proof ID.

        :param proof_id: The ID of the proof to update.
        :param file_path: Path to the new version of the proof file.
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data of the updated proof.
        """
        with open(file_path, 'rb') as file:
            files = {'file': file}
            return self.client.post(self.BASE_URL, f"/{proof_id}/versions", files=files, raw=raw)
