"""
Data Class representing CampaignData
"""
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class CampaignData:
    """
    Skeleton for deserializing CampaignDataList
    """
    campaign_name: str
    number_type: str
    campaign_type: str
    test_type: str
    view_on_jobtester: list[str]
    IVR_traversal: str = None
    interstate_testing: bool = None
    max_calls_per_number: str = None
    test_state:str = None
