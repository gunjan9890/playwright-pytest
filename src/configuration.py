"""
Data class
"""
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class BrowserConfigData:
    """
    Class skeleton for Browser Configuration
    """
    name: str
    headless: bool
    arguments: list[str]
    delay_miliseconds: int
    default_timeout_miliseconds: int
    channel: str = None


@dataclass_json
@dataclass
class ReportConfigData:
    """
    Class skeleton for Report Configuration
    """
    screenshot_on_fail: bool
    screenshot_on_info: bool


@dataclass_json
@dataclass
class ConfigurationData:
    """
    Class skeleton for Configuration.
    """
    # mandatory fields on the top
    browser: BrowserConfigData
    report: ReportConfigData
    aut: dict[str, str]
    api: dict[str, str]
    v6: dict[str, str]
