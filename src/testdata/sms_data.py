"""
Data class
"""
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class SmsData:
    """
    Class skeleton for a SMS Send.
    Fields refer to the fields seen on the SMS Send Emulator
    """
    # mandatory fields on the top
    country: str
    provider: str
    number: str
    message: str

