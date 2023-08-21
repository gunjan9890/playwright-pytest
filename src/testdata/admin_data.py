"""
Data class representing AdminPage
"""

from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass

class AdminData:
    """
    Class skeleton for a Admin user.
    Fields refer to the fields seen on the Add user Dialog
    """
    # mandatory fields
    name: str
    email: str
    time_zone: str
    # optional fields
    company : str = None
    department : str = None
    sms : str = None
    country_code: str =None
    backend_admin: str = None
    role : str = None
    status : str = None
    api_access : str = None
    after_save : str = None

@dataclass_json
@dataclass
class AdminDataList:
    """
    To use the AdminData in json format
    """
    admin_data_list: dict[str, AdminData]
