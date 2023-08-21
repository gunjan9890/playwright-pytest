"""
Data Class
"""
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from spearline_qa_src.testdata.campaigns_data import CampaignData
from spearline_qa_src.testdata.campaigns_schedule_data import CampaignScheduleData
from spearline_qa_src.testdata.numbers_data import NumberData
from spearline_qa_src.testdata.expected_data import ExpectedValue
from spearline_qa_src.testdata.admin_data import AdminData
from spearline_qa_src.testdata.sms_data import SmsData
from spearline_qa_src.testdata.staff_notification_data import NotificationData


@dataclass_json()
@dataclass
class GlobalData:
    """
    Skeleton for deserializing global_data.json
    """
    number_data_list: dict[str, NumberData]
    campaign_data_list: dict[str, CampaignData]
    sms_data_list: dict[str,SmsData]
    admin_data_list: dict[str, AdminData]
    staff_notification_data_list: dict[str, NotificationData]
    expected_value: ExpectedValue
    campaign_schedule_data_list: dict[str, CampaignScheduleData]
