"""
Data class
"""
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class NumberData:
    """
    Class skeleton for a Number.
    Fields refer to the fields seen on the Add Number Dialog
    """
    # mandatory fields on the top
    number_type: str
    number: str
    country: str
    toll_status: str
    # optional fields in the end
    phone_group: str = None
    bridge: str = None
    region: str = None
    IVR_traversal: str = None
    carrier: str = None
    location: str = None
    customer: str = None
    department: str = None
    sub_region: str = None
    tag: str = None
    tag2: str = None
    time_matrix: str = None
    time_constraints: str = None
    timezone: str = None
    test_type: str = None
    IVR_description: str = None
    number_time_group: str = None
    minimum_duration: str = None
    silence_threshold: str = None
    silence_timeout: str = None
    language: str = None 
    agent: str = None
    status: str = None
    send_report: str = None
    after_save: str = None
    ivr_description: str = None
    # applications: list[str]
    # sub_tree: dict

@dataclass()
class NumberDataList:
    number_data_list: dict[str, NumberData]