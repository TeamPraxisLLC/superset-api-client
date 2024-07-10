"""Tags."""
from dataclasses import dataclass
from typing import Optional

from supersetapiclient.base import Object, ObjectFactories, raise_for_status


@dataclass
class Tag(Object):
    JSON_FIELDS = []

    id: Optional[int] = None
    name: str = ""
    type: Optional[int] = None
    description: str = ""

class Tags(ObjectFactories):
    endpoint = "tag/"
    base_object = Tag

    @property
    def add_columns(self):
        return ["name", "description"]

    def tag_dashboard(self, dashboard_id, tags):
        """Add tags to a dashboard"""
        # Note: dashboard type is 3 (see ObjectType in superset/tags/models.py)
        url = self.client.join_urls(self.base_url, "3", dashboard_id)
        response = self.client.post(url, json={ "properties": { "tags": tags } })
        raise_for_status(response)

    def untag_dashboard(self, dashboard_id, tag):
        """Remove a tag from a dashboard"""
        # Note: dashboard type is 3 (see ObjectType in superset/tags/models.py)
        url = self.client.join_urls(self.base_url, "3", dashboard_id, tag)
        response = self.client.delete(url)
        raise_for_status(response)
