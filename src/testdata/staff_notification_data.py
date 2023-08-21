"""
Data class representing Staff Zone Notification
"""
from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class NotificationData:
    """
    Class skeleton for add a Notification.
    Fields refer to the fields seen on the Add notification Dialog
    """
    # mandatory fields
    notification: str
    # optional fields
    title : str = None
    url : str = None
    notification_from : str = None
    notification_to: str =None
    backend_admin: str = None

@dataclass_json
@dataclass
class NotificationDataList:
    """
    To use the NotificationData in json format
    """
    staff_notification_data_list: dict[str, NotificationData]
