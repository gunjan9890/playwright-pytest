"""
Data Class representing CommonData on the platform
"""
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class ExpectedValue:
    """
    Skeleton for deserializing Expected values
    """
    admin_url: str
    admin_add_user_success_msg: str
    admin_delete_user_success_msg: str
    notification_add_success_msg: str
    notification_delete_success_msg: str
    campaign_table_headers: list[str]
