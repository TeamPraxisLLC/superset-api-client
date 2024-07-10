"""Roles."""
from dataclasses import dataclass
from typing import Optional

from supersetapiclient.base import Object, ObjectFactories, raise_for_status


@dataclass
class Role(Object):
    JSON_FIELDS = []

    id: Optional[int] = None
    name: str = ""

class Roles(ObjectFactories):
    endpoint = "security/roles/"
    base_object = Role
