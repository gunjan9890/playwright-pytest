"""
Generating the testdata automatically
"""
import dataclasses
import datetime
import random
from dataclasses_json import dataclass_json

from spearline_qa_src.testdata.campaigns_data import CampaignData
from spearline_qa_src.testdata.campaigns_schedule_data import CampaignScheduleData
from spearline_qa_src.testdata.global_data import GlobalData
from spearline_qa_src.testdata.numbers_data import NumberData
from spearline_qa_src.testdata.sms_data import SmsData


@dataclass_json
@dataclasses.dataclass
class MyClass:
    """
    class representing dictionary of NumberData to generate json
    """
    number_data_list: dict[str, NumberData]


def generate_test_data():
    """
    Method to generate NumberData list based on different combinations
    :return:
    """

    t = GlobalData(number_data_list=generate_number_data(),
                   campaign_data_list=generate_campaign_data(),
                   sms_data_list=generate_sms_data(),
                   admin_data_list=None,
                   expected_value=generate_expected_values(),
                   campaign_schedule_data_list=generate_campaign_schedule_data(),
                   staff_notification_data_list=None
                   )
    print(t.to_json(indent=4))


def generate_number_data():
    """
    Generate NumberData
    :return: dict[str, NumberData]
    """
    number_types = ['PSTN Conference Quality', 'PSTN Quality', 'IVR', 'External Quality', 'SIP Conference Quality',
                    'SIP Quality', 'Outbound Conference Quality', 'IHG IVR']
    toll_status = ['Toll', 'Toll Free']
    ivr_traversal = ['Spearline Prompt', 'Skype Test']
    country = ['India', 'Ireland']
    time_matrix = ['Every Minute', 'Every Hour', 'Every Day']
    time_constraints = ['Initial Test 24/7', 'Opening Hours']

    my_dict = {}
    counter = 0

    for n_type in number_types:
        for t_status in toll_status:
            for i_traversal in ivr_traversal:
                counter += 1
                if n_type == "PSTN Conference Quality":
                    c = country[counter%(len(country))]
                    tzone = "India - New Delhi" if c == "India" else "Ireland - Dublin"
                    my_dict['iteration' + str(counter)] = NumberData(number_type=n_type,
                                             number=str(random.randint(6000000000, 9999999999)),
                                             country=c, toll_status=t_status,
                                             phone_group='auto phn group', bridge='auto bridge', region='auto region',
                                             IVR_traversal=i_traversal, carrier='auto carrier', location = 'auto location',
                                             customer='auto customer', department='auto department', sub_region='auto sub-region',
                                             tag='auto tag', tag2=None, time_matrix=time_matrix[counter%(len(time_matrix))],
                                             time_constraints=time_constraints[counter%(len(time_constraints))], timezone=tzone,
                                             test_type='Single Line Test', status='Running', send_report='Do not send',
                                             after_save='Add a new number', number_time_group=None, ivr_description=None,
                                             minimum_duration=None, silence_threshold=None, silence_timeout=None, language=None, agent=None,
                                             )
                elif n_type == "PSTN Quality":
                    c = country[counter%(len(country))]
                    tzone = "India - New Delhi" if c == "India" else "Ireland - Dublin"
                    my_dict['iteration' + str(counter)] = NumberData(number_type=n_type,
                                             number=str(random.randint(6000000000, 9999999999)),
                                             country=c, toll_status=t_status,
                                             phone_group=None, bridge=None, region=None,
                                             IVR_traversal=i_traversal, carrier='auto carrier', location = 'auto location',
                                             customer='auto customer', department='auto department', sub_region=None,
                                             tag='auto tag', tag2='auto tag2', time_matrix=time_matrix[counter%(len(time_matrix))],
                                             time_constraints=time_constraints[counter%(len(time_constraints))], timezone=tzone,
                                             test_type='Conference', status='Running', send_report='Do not send',
                                             after_save='Add a new number', number_time_group=None, ivr_description=None,
                                             minimum_duration=None, silence_threshold=None, silence_timeout=None, language=None, agent=None,
                                             )
                elif n_type == "IVR":
                    c = country[counter%(len(country))]
                    tzone = "India - New Delhi" if c == "India" else "Ireland - Dublin"
                    my_dict['iteration' + str(counter)] = NumberData(number_type=n_type,
                                             number=str(random.randint(6000000000, 9999999999)),
                                             country=c, toll_status=t_status,
                                             phone_group=None, bridge=None, region=None,
                                             IVR_traversal=i_traversal, carrier='auto carrier', location = 'auto location',
                                             customer='auto customer', department='auto department', sub_region=None,
                                             tag='auto tag', tag2=None, time_matrix=time_matrix[counter%(len(time_matrix))],
                                             time_constraints=time_constraints[counter%(len(time_constraints))], timezone=tzone,
                                             test_type='Single Line Test', status='Running', send_report='Do not send',
                                             after_save='Add a new number', number_time_group='Test Timegroup', ivr_description='Test ivr Description',
                                             minimum_duration='10', silence_threshold='2', silence_timeout='20', language='English', agent='English Prompt',
                                             )
                elif n_type == "External Quality":
                    c = country[counter%(len(country))]
                    tzone = "India - New Delhi" if c == "India" else "Ireland - Dublin"
                    my_dict['iteration' + str(counter)] = NumberData(number_type=n_type,
                                             number=str(random.randint(6000000000, 9999999999)),
                                             country=c, toll_status=t_status,
                                             phone_group=None, bridge=None, region=None,
                                             IVR_traversal=None, carrier='auto carrier', location = 'auto location',
                                             customer='auto customer', department='auto department', sub_region=None,
                                             tag='auto tag', tag2=None, time_matrix=time_matrix[counter%(len(time_matrix))],
                                             time_constraints=time_constraints[counter%(len(time_constraints))], timezone=tzone,
                                             test_type='External outbound', status='Running', send_report='Do not send',
                                             after_save='Add a new number', number_time_group=None, ivr_description=None,
                                             minimum_duration=None, silence_threshold=None, silence_timeout=None, language=None, agent=None,
                                             )
                elif n_type == "SIP Conference Quality":
                    c = country[counter%(len(country))]
                    tzone = "India - New Delhi" if c == "India" else "Ireland - Dublin"
                    t_status = "SIP"
                    my_dict['iteration' + str(counter)] = NumberData(number_type=n_type,
                                             number=str(random.randint(6000000000, 9999999999)),
                                             country=c, toll_status=t_status,
                                             phone_group='auto phn group', bridge='auto bridge', region='auto region',
                                             IVR_traversal=i_traversal, carrier='auto carrier', location = 'auto location',
                                             customer='auto customer', department='auto department', sub_region='auto sub-region',
                                             tag='auto tag', tag2=None, time_matrix=time_matrix[counter%(len(time_matrix))],
                                             time_constraints=time_constraints[counter%(len(time_constraints))], timezone=tzone,
                                             test_type='SIP Conference', status='Running', send_report='Do not send',
                                             after_save='Add a new number', number_time_group=None, ivr_description=None,
                                             minimum_duration=None, silence_threshold=None, silence_timeout=None, language=None, agent=None,
                                             )
                elif n_type == "SIP Quality":
                    c = country[counter%(len(country))]
                    tzone = "India - New Delhi" if c == "India" else "Ireland - Dublin"
                    t_status = "SIP"
                    my_dict['iteration' + str(counter)] = NumberData(number_type=n_type,
                                             number=str(random.randint(6000000000, 9999999999)),
                                             country=c, toll_status=t_status,
                                             phone_group=None, bridge=None, region=None,
                                             IVR_traversal=i_traversal, carrier='auto carrier', location = 'auto location',
                                             customer='auto customer', department='auto department', sub_region=None,
                                             tag='auto tag', tag2=None, time_matrix=time_matrix[counter%(len(time_matrix))],
                                             time_constraints=time_constraints[counter%(len(time_constraints))], timezone=tzone,
                                             test_type='SIP Endpoint', status='Running', send_report='Do not send',
                                             after_save='Add a new number', number_time_group=None, ivr_description=None,
                                             minimum_duration=None, silence_threshold=None, silence_timeout=None, language=None, agent=None,
                                             )
                elif n_type == "Outbound Conference Quality":
                    c = country[counter%(len(country))]
                    tzone = "India - New Delhi" if c == "India" else "Ireland - Dublin"
                    my_dict['iteration' + str(counter)] = NumberData(number_type=n_type,
                                             number=str(random.randint(6000000000, 9999999999)),
                                             country=c, toll_status=t_status,
                                             phone_group='auto phn group', bridge='auto bridge', region='auto region',
                                             IVR_traversal=i_traversal, carrier='auto carrier', location = 'auto location',
                                             customer='auto customer', department='auto department', sub_region='auto sub-region',
                                             tag='auto tag', tag2=None, time_matrix=time_matrix[counter%(len(time_matrix))],
                                             time_constraints=time_constraints[counter%(len(time_constraints))], timezone=tzone,
                                             test_type='PGI', status='Running', send_report='Do not send',
                                             after_save='Add a new number', number_time_group=None, ivr_description=None,
                                             minimum_duration=None, silence_threshold=None, silence_timeout=None, language=None, agent=None,
                                             )


    return my_dict

def generate_campaign_data():
    """
    Generate CampaignData
    :return: dict[str, CampaignData]
    """
    number_types = ['PSTN Conference Quality', 'PSTN Quality', 'IVR', 'External Quality', 'SIP Conference Quality',
                    'SIP Quality', 'Outbound Conference Quality', 'IHG IVR']
    test_types = {
        "PSTN Conference Quality": ["Conference", "Conference Long Call", "Conference With dynamic prompt",
                                    "Link Test", "Outbound Conference"],
        "PSTN Quality": ["Agent Connection Test", "Connection", "Multi-prompt"],
        "IVR": ["IVR Map", "IVR Traversal with Prompts"],
        "External Quality": ["External outbound", "Google Agent"],
        "SIP Conference Quality": ["SIP Conference"],
        "SIP Quality": ["SIP Call Forward", "SIP Endpoint"],
        "Outbound Conference Quality": ["Gartner Outbound", "PGI Outbound"],
        "IHG IVR": ["IVR Type", "IVR Type -Phase2 (Updated)"]
    }

    ivr_traversal = {
        "PSTN Conference Quality": ["Connection Test", "Skype Test", "Spearline Prompt"],
        "PSTN Quality": ["Connection Wait 15", "Skype Test", "Spearline Prompt"],
        "IVR": ["Skype Test", "Spearline Prompt"],
        "External Quality": ["External outbound", "Google Agent"],
        "SIP Conference Quality": ["SIP Conference"],
        "SIP Quality": ["SIP Call Forward", "SIP Endpoint"],
        "Outbound Conference Quality": ["Gartner Outbound", "PGI Outbound"],
        "IHG IVR": ["IVR Type", "IVR Type -Phase2 (Updated)"]
    }

    states = {"New York - New York", "Minnesota - Minneapolis"}

    my_dict = {}
    counter = 0

    for n_type in number_types:
        for t_type in test_types[n_type]:
            for i_traversal in ivr_traversal[n_type]:
                counter += 1
                intr_state_tst = None if n_type == "PSTN Conference Quality" else True if counter % 2 == 0 else False
                my_dict['iteration' + str(counter)] = CampaignData(
                    campaign_name=n_type.replace(" ", "") + str(DateUtils.get_timestamp()),
                    number_type=n_type,
                    campaign_type="PSTN" if counter % 2 == 0 else "GSM",
                    test_type=t_type,
                    view_on_jobtester=["qa.service@spearline.com", "gunjan.sheth@spearline.com"],
                    IVR_traversal=i_traversal,
                    interstate_testing= intr_state_tst,
                    max_calls_per_number=str(random.randint(10, 99)),
                    test_state= "New York - New York" if intr_state_tst else None
                )

    return my_dict


def generate_sms_data():
    countries = {"Australia": "Telstra Mobile", "India": "AirTel", "Ireland": "Vodafone",
                 "United States": "att-yeastar-usa-nev1-m1-5"}
    messages = ["Simple One Line Message",
                "Double Line Message with New Line\nLine 1\nLine 2",
                "abcde fghi" * 10,
                "महान कम"]

    my_dict = {}
    counter = 0
    for message in messages:
        counter += 1
        my_dict['iteration' + str(counter)] = SmsData(country=list(countries.keys())[counter % (len(countries))],
                                                      provider=list(countries.values())[counter % (len(countries))],
                                                      number=str(random.randint(7000000000, 9999999999)),
                                                      message=messages[counter % (len(messages))])
    return my_dict


def generate_common_data():
    my_dict = {"key1": "value1", "key2": "value2", "key3": "value3"}
    return my_dict


def generate_expected_values():
    my_dict = {
        "admin_url": "https://qa-staging.spearline.com/admin/user",
        "admin_add_user_success_msg": "The user has been saved.",
        "admin_delete_user_success_msg": "The user has been deleted.",
        "notification_add_success_msg": "The spearline notification has been saved.",
        "notification_delete_success_msg": "The spearline notification has been deleted.",
        "campaign_table_headers": ["Name", "Campaign Type", "Start On", "End On", "Test Type", "Time Zone",
                                   "Report Interval", "Is Approved", "Job Count", "Campaign Time Group", "Lsat Run",
                                   "Created By", "Created On", "Status", "Monthly Test Count", "Actions"]
    }
    return my_dict


def generate_campaign_schedule_data():
    number_types = ['PSTN Conference Quality', 'PSTN Quality', 'IVR', 'External Quality', 'SIP Conference Quality',
                    'SIP Quality', 'Outbound Conference Quality', 'IHG IVR']
    time_zones = ["Ireland - Dublind", "India - New Delhi"]
    send_repo = ["Do not send", "After Job has completed", "After Job has completed and any test has failed",
                 "After Job has completed and all tests have failed", "If all failed same as present"]

    my_dict = {}
    counter = 0
    for n_type in number_types:

        if n_type in ["IVR", "IHG IVR"]:
            for _once_off in [True, False]:
                for _interval in ["Every Week", "Every Month"]:
                    counter += 1
                    if _once_off:
                        temp_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                        my_dict['iteration' + str(counter)] = \
                            CampaignScheduleData(number_type=n_type, once_off_campaign=_once_off, start_on=temp_time,
                                                 end_on=None, interval=None, timezone=None, send_report=None,
                                                 email_to=None, email_cc=None, time_group=None, run_now=None)
                    else:
                        temp_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                        temp_time2 = (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).strftime(
                            "%Y-%m-%d %H:%M:%S")
                        my_dict['iteration' + str(counter)] = \
                            CampaignScheduleData(number_type=n_type, once_off_campaign=_once_off, start_on=temp_time,
                                                 end_on=temp_time2, interval=_interval, timezone=None,
                                                 send_report=_send_report, email_to="qa.service@spearline.com",
                                                 email_cc="gunjan.sheth@spearline.com", time_group=None,
                                                 run_now=_run_now)
        else:
            for _send_report in send_repo:
                for _once_off in [True, False]:
                    for _run_now in [True, False]:
                        counter += 1
                        temp_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                        if _run_now:
                            my_dict['iteration' + str(counter)] = \
                                CampaignScheduleData(number_type=n_type, once_off_campaign=_once_off,
                                                     start_on=temp_time,
                                                     end_on=None, interval=None, timezone=None,
                                                     send_report=_send_report, email_to="qa.service@spearline.com",
                                                     email_cc="gunjan.sheth@spearline.com", time_group=None,
                                                     run_now=_run_now)
                        else:
                            my_dict['iteration' + str(counter)] = \
                                CampaignScheduleData(number_type=n_type, once_off_campaign=_once_off,
                                                     start_on=temp_time,
                                                     end_on=None, interval=None, timezone=time_zones[counter % 2],
                                                     send_report=_send_report, email_to="qa.service@spearline.com",
                                                     email_cc="gunjan.sheth@spearline.com", time_group=None,
                                                     run_now=_run_now)
    return my_dict


generate_test_data()
# print(generate_campaign_data())
