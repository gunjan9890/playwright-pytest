"""
A Base Class for Getting common Settings required throughout the Execution
"""
import os
from pathlib import Path
import inspect

from playwright.sync_api import Browser, Page, sync_playwright, APIRequestContext, BrowserContext

from spearline_qa_src.configuration import ConfigurationData
from spearline_qa_src.lib.test_listener import TestListener
from spearline_qa_src.testdata.global_data import GlobalData


class TestBase:
    """
    BaseClass for getting Browser, Page, Configuration, TestData & Other Reusable Functions
    """
    __browser: Browser = None
    __api_context: BrowserContext = None
    __page: Page = None
    __config: ConfigurationData = None
    __project_root_path = None
    __screenshot_folder_path = None
    __project_name = "spearline_qa_src"
    __screenshot_folder = os.path.join("allure-results", "screenshots")
    __screenshot_counter = 1
    __dict = {}
    __test_data = None
    __play = None

    @staticmethod
    def __get_playwright():
        if TestBase.__play is None:
            TestBase.__play = sync_playwright().start()
        return TestBase.__play

    @staticmethod
    def get_browser():
        """
        Method to get current or new instance of Browser. Will return a new instance only if the previous was
        closed or never initialized
        :return: Browser
        """

        if TestBase.__browser is None or not TestBase.__browser.is_connected():
            # the configurations can be coming from a JSON or YML file
            headless_val = TestBase.__config.browser.headless
            slow_mo_val = TestBase.__config.browser.delay_miliseconds
            args_val = TestBase.__config.browser.arguments
            channel_val = TestBase.__config.browser.channel
            if TestBase.__config.browser.name == "chromium":
                TestBase.__browser = TestBase.__get_playwright().chromium.launch(
                    headless=headless_val, slow_mo=slow_mo_val, args=args_val, channel=channel_val)
            elif TestBase.__config.browser.name == "firefox":
                TestBase.__browser = TestBase.__get_playwright().firefox.launch(
                    headless=headless_val, slow_mo=slow_mo_val, args=args_val, channel=channel_val)
            elif TestBase.__config.browser.name == "webkit":
                TestBase.__browser = TestBase.__get_playwright().webkit.launch(
                    headless=headless_val, slow_mo=slow_mo_val, args=args_val, channel=channel_val)
        return TestBase.__browser

    @staticmethod
    def get_page():
        """
        Method to get current or new instance of Page. Will return a new instance only if the previous was
        closed or never initialized
        :return: Page
        """
        if TestBase.__page is None or (TestBase.__page.is_closed()):
            TestBase.__page = TestBase.get_browser().new_page()
            TestBase.__page.set_default_timeout(timeout=TestBase.get_config().browser.default_timeout_miliseconds)
        return TestBase.__page

    @staticmethod
    def get_api_context() -> APIRequestContext:
        """
        Method to get current or new instance of BrowserContext that will be used to make API requests
        :return:
        """
        if TestBase.__api_context is None:
            api_base_url = TestBase.get_config().api[TestBase.get_config().api["environment"]]
            TestBase.__api_context = TestBase.get_browser().new_context(base_url=api_base_url)
        return TestBase.__api_context.request

    @staticmethod
    def take_screenshot(ref_name: str = "snap", full_page: bool = True):
        """
        Pending
        :param full_page:
        :param ref_name:
        :return:
        """
        if TestBase.__page is not None and not TestBase.__page.is_closed():
            if TestListener.current_test_case_request is None:
                # used for taking a screenshot during precondition, as the current testcase can be none
                node_parent = TestListener.current_test_module_request.node.parent.name
                node_self = TestListener.current_test_module_request.node.name
            else:
                node_parent = TestListener.current_test_case_request.node.parent.name
                node_self = TestListener.current_test_case_request.node.name
            file_name = node_parent + "." + node_self + "." + ref_name + "." + \
                        str(TestBase.__screenshot_counter).rjust(4, "0") + ".png"
            screenshot_path = os.path.join(TestBase.get_project_root_path(), TestBase.__screenshot_folder, file_name)
            shot = TestBase.__page.screenshot(type="png", path=screenshot_path, full_page=full_page)

            # increment the screenshot count
            TestBase.__screenshot_counter += 1
            return shot
        return None

    @staticmethod
    def get_project_root_path() -> str:
        """
        Gives the Project Root location till "spearline_qa_src"
        :return: str
        """
        if TestBase.__project_root_path is None:
            if TestBase.__project_name in str(Path.cwd().absolute()):
                # check if the current absolute path has the name of the Project somewhere in it
                cwd = Path.cwd()
                while (cwd.name != TestBase.__project_name) and (str(cwd.absolute()) != cwd.drive + cwd.root):
                    cwd = cwd.parent
                TestBase.__project_root_path = cwd.absolute()
            else:
                # current execution might be happening from parent of this Project directory
                cwd = Path.cwd()
                current_children = os.listdir(cwd.absolute())
                for folder in current_children:
                    if Path(os.path.join(str(cwd.absolute()), folder)).is_dir() and folder == TestBase.__project_name:
                        TestBase.__project_root_path = os.path.join(cwd.absolute(), folder)
        return TestBase.__project_root_path

    @staticmethod
    def set_value(key, value) -> None:
        """
        Temporarily store a variable / object during Test Execution, can be retrived using get_value
        :param key: unique key to identify your object later
        :param value: value for the key
        :return: None
        """
        TestBase.__dict[key] = value

    @staticmethod
    def get_value(key) -> object:
        """
        Retrieves the stored object in the dictionary object
        :param key: unique key to identify your object
        :return: value for your key, if the key is not present will throw KeyNotFound Error
        """
        return TestBase.__dict[key]

    @staticmethod
    def get_test_data() -> GlobalData:
        """
        Reads and returns TestData object based on the 'testdata/global_data.json'
        :return: GlobalData
        """
        if TestBase.__test_data is None:
            TestBase.__test_data = TestBase.__read_test_data()
        return TestBase.__test_data

    @staticmethod
    def __read_test_data():
        """
        Internal method to read TestData once
        :return: GlobalData
        """
        sample_json_file = os.path.join(TestBase.get_project_root_path(), "testdata/global_data.json")
        json_file = open(sample_json_file, "r").read()
        return GlobalData.from_json(json_file)

    @staticmethod
    def open_new_tab():
        """
        Opens new tab in the same browser context
        """
        with TestBase.get_page().expect_popup() as popup:
            TestBase.get_page().click("a[target='_blank']")
        return popup.value

    @staticmethod
    def create_instance(class_name: str, instance: str):
        """
        Creates instances for all the locators present in Page Locator file
        """
        for attr in inspect.getmembers(instance):
            if not attr[0].startswith('_'):
                if not inspect.ismethod(attr[1]):
                    setattr(class_name, attr[0], TestBase.get_page().locator(attr[1]))

    @staticmethod
    def set_config(config_map: ConfigurationData) -> None:
        """
        Sets the Configuration object
        :param config_map:
        :return:
        """
        TestBase.__config = config_map

    @staticmethod
    def get_config() -> ConfigurationData:
        """
        Gets the Configuration object
        :return:
        """
        return TestBase.__config
