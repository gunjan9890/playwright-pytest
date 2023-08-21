"""
Data Class representing CampaignData
"""
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class CampaignScheduleData:
    """
    Skeleton for deserializing CampaignDataList
    """
    number_type:str = None
    once_off_campaign:bool = None
    start_on:str = None
    end_on:str = None
    interval:str = None
    timezone:str = None
    send_report:str = None
    email_to:str = None
    email_cc:str = None
    time_group:str = None
    run_now:bool = None
