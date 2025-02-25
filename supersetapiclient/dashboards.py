"""Dashboards."""
from dataclasses import dataclass, field
from typing import List, Optional

from supersetapiclient.base import Object, ObjectFactories, default_string, json_field, raise_for_status

@dataclass
class DashboardEmbed(Object):
    allowed_domains: List[str] = field(default_factory=list)
    uuid:str = None

@dataclass
class Dashboard(Object):
    JSON_FIELDS = ["json_metadata", "position_json"]

    dashboard_title: str
    published: bool
    id: Optional[int] = None
    json_metadata: dict = json_field()
    position_json: dict = json_field()
    changed_by: str = default_string()
    slug: str = default_string()
    changed_by_name: str = default_string()
    changed_by_url: str = default_string()
    css: str = default_string()
    changed_on: str = default_string()
    charts: List[str] = field(default_factory=list)
    tags: List[object] = field(default_factory=list)
    roles: List[object] = field(default_factory=list)

    @property
    def colors(self) -> dict:
        """Get dashboard color mapping."""
        return self.json_metadata.get("label_colors", {})

    @colors.setter
    def colors(self, value: dict) -> None:
        """Set dashboard color mapping."""
        self.json_metadata["label_colors"] = value

    def update_colors(self, value: dict) -> None:
        """Update dashboard colors."""
        colors = self.colors
        colors.update(value)
        self.colors = colors

    def get_charts(self) -> List[int]:
        """Get chart objects"""
        charts = []
        for slice_name in self.charts:
            c = self._parent.client.charts.find_one(slice_name=slice_name)
            charts.append(c)
        return charts

    def get_embed(self) -> DashboardEmbed:
        """Get the dashboard's embedded configuration"""
        client = self._parent.client
        url = client.join_urls(self.base_url,"embedded")
        response = client.get(url)
        if response.status_code == 404:
            return None
        return DashboardEmbed().from_json(response.json().get("result"))

    def create_embed(self, allowed_domains: List[str]) -> DashboardEmbed:
        """Set a dashboard's embedded configuration"""
        client = self._parent.client
        url = client.join_urls(self.base_url,"embedded")
        response = client.post(url, json={ "allowed_domains": allowed_domains })
        raise_for_status(response)
        return DashboardEmbed().from_json(response.json().get("result"))

    def save(self) -> None:
        """Override save to fix roles array."""
        if self.roles and len(self.roles) > 0 and isinstance(self.roles[0], dict):
            self.roles = list(map(lambda x: x["id"], self.roles))
        return super().save()

class Dashboards(ObjectFactories):
    endpoint = "dashboard/"
    base_object = Dashboard
