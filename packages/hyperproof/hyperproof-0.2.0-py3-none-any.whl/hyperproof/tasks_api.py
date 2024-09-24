# hyperproof/tasks_api.py
from .utils import APIClient

class TasksAPI:
    """
    This class handles interactions with the Tasks API of Hyperproof.
    It allows for creating, retrieving, updating tasks, and handling task-related proofs.
    """
    BASE_URL = "https://api.hyperproof.app/v1/tasks"

    def __init__(self, client_id, client_secret):
        # Initialize the API client with authentication
        self.client = APIClient(client_id, client_secret)

    def add_task(self, title, target_object, description, assignee_id, priority, due_date, has_integration=False, raw=False):
        """
        Adds a new task to an organization.

        :param title: Title of the task.
        :param target_object: Target object (includes objectId and objectType).
        :param description: Description of the task.
        :param assignee_id: ID of the assignee.
        :param priority: Priority of the task ('highest', 'high', 'medium', 'low', 'lowest').
        :param due_date: Due date of the task (ISO 8601 format).
        :param has_integration: Boolean indicating if the task has an integration (default is False).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        data = {
            "title": title,
            "targetObject": target_object,
            "description": description,
            "assigneeId": assignee_id,
            "priority": priority,
            "dueDate": due_date,
            "hasIntegration": has_integration
        }
        return self.client.post(self.BASE_URL, "/", data=data, raw=raw)

    def get_task_by_id(self, task_id, raw=False):
        """
        Retrieves a task in an organization by ID.

        :param task_id: The unique ID of the task to retrieve.
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        return self.client.get(self.BASE_URL, f"/{task_id}", raw=raw)

    def update_task(self, task_id, title=None, description=None, assignee_id=None, target_id=None, target_type=None,
                    task_status_id=None, priority=None, sort_order=None, due_date=None, raw=False):
        """
        Updates an existing task with new values.

        :param task_id: The unique ID of the task to update.
        :param title: New title for the task (optional).
        :param description: New description of the task (optional).
        :param assignee_id: New assignee ID (optional).
        :param target_id: New target object ID (optional).
        :param target_type: New target object type (optional).
        :param task_status_id: New task status ID (optional).
        :param priority: New priority of the task ('highest', 'high', 'medium', 'low', 'lowest', optional).
        :param sort_order: New sort order (optional).
        :param due_date: New due date (ISO 8601 format, optional).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        data = {
            "title": title,
            "description": description,
            "assigneeId": assignee_id,
            "targetId": target_id,
            "targetType": target_type,
            "taskStatusId": task_status_id,
            "priority": priority,
            "sortOrder": sort_order,
            "dueDate": due_date
        }
        return self.client.patch(self.BASE_URL, f"/{task_id}", data=data, raw=raw)

    def add_task_proof(self, task_id, file_path, proof_owned_by=None, proof_source=None, proof_source_id=None,
                       proof_source_file_id=None, proof_source_modified_on=None, proof_live_sync_enabled=False, raw=False):
        """
        Adds a proof item to a task.

        :param task_id: The unique ID of the task.
        :param file_path: Path to the proof file to upload.
        :param proof_owned_by: ID of the proof owner (optional).
        :param proof_source: Source of the proof (optional).
        :param proof_source_id: ID of the proof source (optional).
        :param proof_source_file_id: Source file ID of the proof (optional).
        :param proof_source_modified_on: Date and time the proof was modified (ISO 8601 format, optional).
        :param proof_live_sync_enabled: Whether live sync is enabled for the proof (optional, default is False).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        with open(file_path, 'rb') as file:
            files = {'proof': file}
            data = {
                "hp-proof-owned-by": proof_owned_by,
                "hp-proof-source": proof_source,
                "hp-proof-source-id": proof_source_id,
                "hp-proof-source-file-id": proof_source_file_id,
                "hp-proof-source-modified-on": proof_source_modified_on,
                "hp-proof-live-sync-enabled": proof_live_sync_enabled
            }
            return self.client.post(self.BASE_URL, f"/{task_id}/proof", files=files, data=data, raw=raw)

    def get_task_proof_metadata(self, task_id, raw=False):
        """
        Retrieves the proof metadata associated with a task.

        :param task_id: The unique ID of the task.
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        return self.client.get(self.BASE_URL, f"/{task_id}/proof", raw=raw)

    def filter_tasks(self, target_object_type=None, target_object_ids=None, task_ids=None, assignee_ids=None, modified_after=None, raw=False):
        """
        Gets the set of tasks matching the supplied filter.

        :param target_object_type: Type of the target object (optional).
        :param target_object_ids: List of target object IDs to filter by (optional).
        :param task_ids: List of task IDs to filter by (optional).
        :param assignee_ids: List of assignee IDs to filter by (optional).
        :param modified_after: Return tasks modified after this date (ISO 8601 format, optional).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        data = {
            "targetObjectType": target_object_type,
            "targetObjectIds": target_object_ids or [],
            "taskIds": task_ids or [],
            "assigneeIds": assignee_ids or [],
            "modifiedAfter": modified_after
        }
        return self.client.put(self.BASE_URL, "/filter", data=data, raw=raw)

    def get_task_comments(self, task_id, raw=False):
        """
        Retrieves the comments in a task's activity feed.

        :param task_id: The unique ID of the task.
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        return self.client.get(self.BASE_URL, f"/{task_id}/comments", raw=raw)

    def add_task_comment(self, task_id, comment_text_formatted, is_internal_comment=False, object_type="task", object_id=None, raw=False):
        """
        Adds a comment to a task's activity feed.

        :param task_id: The unique ID of the task.
        :param comment_text_formatted: Formatted comment text.
        :param is_internal_comment: Whether it's an internal comment (default is False).
        :param object_type: Type of the object associated with the comment (default is 'task').
        :param object_id: The object ID associated with the comment (optional).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        data = {
            "commentTextFormatted": comment_text_formatted,
            "isInternalComment": is_internal_comment,
            "objectType": object_type,
            "objectId": object_id
        }
        return self.client.post(self.BASE_URL, f"/{task_id}/comments", data=data, raw=raw)

    def update_task_comment(self, task_id, comment_id, comment_text_formatted=None, is_internal_comment=None, object_type="task", object_id=None, raw=False):
        """
        Updates an existing comment in a task's activity feed.

        :param task_id: The unique ID of the task.
        :param comment_id: The unique ID of the comment.
        :param comment_text_formatted: Updated formatted comment text (optional).
        :param is_internal_comment: Updated internal comment flag (optional).
        :param object_type: Type of the object associated with the comment (default is 'task').
        :param object_id: The object ID associated with the comment (optional).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        data = {
            "commentTextFormatted": comment_text_formatted,
            "isInternalComment": is_internal_comment,
            "objectType": object_type,
            "objectId": object_id
        }
        return self.client.patch(self.BASE_URL, f"/{task_id}/comments/{comment_id}", data=data, raw=raw)

    def delete_task_comment(self, task_id, comment_id, raw=False):
        """
        Deletes an existing comment in a task's activity feed.

        :param task_id: The unique ID of the task.
        :param comment_id: The unique ID of the comment.
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        return self.client.delete(self.BASE_URL, f"/{task_id}/comments/{comment_id}", raw=raw)
