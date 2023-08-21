"""
This module has functions to verify different form controls
"""
import csv
import datetime
import inspect
import os
import random
import re
import string
import time
from re import Pattern
from typing import Any

from playwright.sync_api import Locator
from playwright.sync_api import FileChooser

from spearline_qa_src.v5.components.multi_select_dropdown import MultiSelectDropdown
from spearline_qa_src.v5.components.single_select_dropdown import SingleSelectDropdown
from spearline_qa_src.v5.components.spearline_locator import SpearlineLocator
from spearline_qa_src.v5.components.spearline_table import SpearlineTable
from spearline_qa_src.lib.reporter import Reporter
from spearline_qa_src.lib.test_base import TestBase


class VerifyUtils:
    """
    Contains support methods for verification of form elements
    """

    @staticmethod
    def verify_button(locator: Locator, expected_text: str = None, is_enabled: bool = True):
        """
        Method to add basic verifications for a given button element
        :param locator: The locator for which you want to verify
        :param expected_text: The expected text of the button / value of the button
        :param is_enabled: Verify if the button should be enabled or disabled
        :return:
        """
        args = inspect.getframeinfo(inspect.getouterframes(inspect.currentframe())[1][0]).code_context[0].strip()
        variable_name = args[args.find('(') + 1:-1].split(',')[0].split(".")[-1]
        variable_name = " ".join(variable_name.split('_'))
        Reporter.log_step(f"Verification for {variable_name}")
        locator.wait_for(state="visible")
        flag = True
        Reporter.log_sub_step("Verify the button is visible")
        if not locator.is_visible():
            flag = False
            Reporter.log_sub_step("Element is not visible")
        if expected_text:
            button_text = ""
            if locator.get_attribute("value") is not None:
                button_text = locator.get_attribute("value").strip()
            else:
                button_text = locator.text_content().strip()

            d1 = {
                "Expected Text Or Value": expected_text,
                "Actual Text Or Value": button_text + " / " + locator.text_content()
            }
            Reporter.log_sub_step("Verify the button's text / value'", step_params=d1)
            if not (button_text == expected_text.strip() or expected_text.strip() == locator.text_content().strip()):
                flag = False
                Reporter.log_sub_step("Mismatch in button name")
        if is_enabled:
            Reporter.log_sub_step("Verify the button is enabled")
            if not locator.is_enabled():
                flag = False
                Reporter.log_sub_step("Button is not enabled")
        else:
            Reporter.log_sub_step("Verify the button is disabled")
            if locator.is_enabled():
                flag = False
                Reporter.log_sub_step("Button is not disabled")
        assert flag, "One or more assertions failed"

    @staticmethod
    def verify_label(locator: Locator, expected_text: str, href: str = None):
        """
        Method to verify label
        :param locator: The locator for which you want to verify
        :param expected_text: the expected text of the label of the button
        :param href: The expected href, if you want to verify the href
        :return:
        """
        args = inspect.getframeinfo(inspect.getouterframes(inspect.currentframe())[1][0]).code_context[0].strip()
        variable_name = args[args.find('(') + 1:-1].split(',')[0].split(".")[-1]
        variable_name = " ".join(variable_name.split('_'))
        Reporter.log_step(f"Verification for {variable_name}")
        locator.wait_for(state="visible")
        flag = True
        Reporter.log_sub_step(f"Verify the [{expected_text}] label is visible")
        if not locator.is_visible():
            flag = False
            Reporter.log_sub_step("Element is not visible")
        actual_text = locator.text_content().strip()
        d1 = {
            "Expected Text": expected_text,
            "Actual Text": actual_text
        }
        Reporter.log_sub_step("Verify the label text", step_params=d1)
        if actual_text != expected_text:
            flag = False
            Reporter.log_sub_step("Mismatch in label name", attach_screenshot=True)
        if href:
            d2 = {
                "Expected HREF": href,
                "Actual HREF": locator.get_attribute("href")
            }
            Reporter.log_sub_step("Verify href property of the label", step_params=d2)
            if locator.get_attribute("href") != href:
                flag = False
                Reporter.log_sub_step("Mismatch in href", attach_screenshot=True)
        assert flag, "One or more assertions failed"

    @staticmethod
    def verify_checkbox(locator: SpearlineLocator, checkbox_label: str = None, is_required: bool = False,
                        is_checked: bool = False):
        """
        Method to add basic verifications for a given checkbox element
        :param locator: The locator for which you want to verify
        :param checkbox_label: the expected text of the checkbox label
        :param is_required: Expected value if the checkbox is mandatory
        :param is_checked: Expected value if the checkbox should be checked or unchecked
        :return:
        """
        args = inspect.getframeinfo(inspect.getouterframes(inspect.currentframe())[1][0]).code_context[0].strip()
        variable_name = args[args.find('(') + 1:-1].split(',')[0].split(".")[-1]
        variable_name = " ".join(variable_name.split('_'))
        Reporter.log_step(f"Verification for {variable_name}")
        locator.self_object.wait_for(state="visible")
        flag = True
        d1 = {
            "Expected Checkbox's Label Text": checkbox_label,
            "Actual Checkbox's Label Text": locator.get_parents_text()
        }
        Reporter.log_sub_step("Verify the checkbox's label text", step_params=d1)
        if locator.get_parents_text() != checkbox_label:
            flag = False
            Reporter.log_sub_step("Mismatch in checkbox label")
        if is_required:
            Reporter.log_sub_step("Verify the checkbox is required")
            if not locator.self_object.get_attribute("required"):
                flag = False
                Reporter.log_sub_step("Checkbox does not have 'required' attribute")
        if is_checked:
            Reporter.log_sub_step("Verify the checkbox is checked")
            if not locator.self_object.is_checked():
                flag = False
                Reporter.log_sub_step("Checkbox is not checked")
            locator.self_object.uncheck()
            locator.self_object.check()
        else:
            Reporter.log_sub_step("Verify the checkbox is unchecked")
            if locator.self_object.is_checked():
                flag = False
                Reporter.log_sub_step("Checkbox is checked")
            locator.self_object.check()
            locator.self_object.uncheck()
        assert flag, "One or more assertions failed"

    @staticmethod
    def verify_multiple_checkboxes(table_locator: SpearlineTable, checkbox_column: int):
        """
        To verify multiple checkboxes inside a table
        """
        args = inspect.getframeinfo(inspect.getouterframes(inspect.currentframe())[1][0]).code_context[0].strip()
        variable_name = args[args.find('(') + 1:-1].split(',')[0].split(".")[-1]
        variable_name = " ".join(variable_name.split('_'))
        Reporter.log_step(f"Verification for multiple checkboxes inside {variable_name} table")
        row_count = table_locator.get_row_count()
        for index in range(row_count):
            checkbox: Locator = table_locator.get_cell(index, checkbox_column)
            checkbox = checkbox.locator("//input")
            checkbox.check()
            checkbox.uncheck()

    @staticmethod
    def verify_radio_button(locator: SpearlineLocator, radio_label: str = None, is_required: bool = False,
                            is_checked: bool = False):
        """
        Method to add basic verifications for a given radio button element
        :param locator: The locator for which you want to verify
        :param radio_label: the expected text of the label of the button
        :param is_required: Whether the radio button is a mandatory field
        :param is_checked: Whether the radio button should be ON or OFF
        :return:
        """
        args = inspect.getframeinfo(inspect.getouterframes(inspect.currentframe())[1][0]).code_context[0].strip()
        variable_name = args[args.find('(') + 1:-1].split(',')[0].split(".")[-1]
        variable_name = " ".join(variable_name.split('_'))
        Reporter.log_step(f"Verification for {variable_name}")
        locator.self_object.wait_for(state="visible")
        flag = True
        d1 = {
            "Expected Radio Button's Label Text": radio_label,
            "Actual Radio Button's Label Text": locator.get_parents_text()
        }
        Reporter.log_sub_step("Verify the radio button's label text", step_params=d1)
        if locator.get_parents_text() != radio_label:
            flag = False
            Reporter.log_sub_step("Mismatch in radio button label")
        if is_required:
            Reporter.log_sub_step("Verify the radio button is required")
            if not locator.self_object.get_attribute("required"):
                flag = False
                Reporter.log_sub_step("Radio button does not have 'required' attribute")
        if is_checked:
            Reporter.log_sub_step("Verify the radio button is checked")
            if not locator.self_object.is_checked():
                flag = False
                Reporter.log_sub_step("Radio button is not checked")
        else:
            Reporter.log_sub_step("Verify the radio button is unchecked")
            if locator.self_object.is_checked():
                flag = False
                Reporter.log_sub_step("Radio button is checked")
        assert flag, "One or more assertions failed"

    @staticmethod
    def verify_textbox(locator: Locator, is_required: bool = None, input_value: str = None, placeholder: str = None):
        """
        Method to add basic verifications for a given textbox element
        :param locator: The locator for which you want to verify
        :param is_required: Whether the textbox should be mandatory
        :param input_value: the expected value of the textbox
        :param placeholder: the expected placeholder of the textbox
        :return:
        """
        args = inspect.getframeinfo(inspect.getouterframes(inspect.currentframe())[1][0]).code_context[0].strip()
        variable_name = args[args.find('(') + 1:-1].split(',')[0].split(".")[-1]
        variable_name = " ".join(variable_name.split('_'))
        Reporter.log_step(f"Verification for {variable_name}")
        locator.wait_for(state="visible")
        flag = True
        Reporter.log_sub_step("Verify the textbox is visible")
        if not locator.is_visible():
            flag = False
            Reporter.log_sub_step("Textbox is not visible")
        if is_required:
            Reporter.log_sub_step("Verify the textbox is required")
            if not locator.get_attribute("required"):
                flag = False
                Reporter.log_sub_step("Textbox does not have 'required' attribute")
        if placeholder:
            d1 = {
                "Expected Placeholder Value": placeholder,
                "Actual Placeholder Value": locator.get_attribute("placeholder").strip()
            }
            Reporter.log_sub_step("Verify the textbox's placeholder value", step_params=d1)
            actual_value = locator.get_attribute("placeholder").strip()
            if not actual_value == placeholder:
                flag = False
                Reporter.log_sub_step("Mismatch in textbox label")
        if input_value:
            locator.fill("")
            locator.fill(input_value)
            d2 = {
                "Expected Input Value": input_value,
                "Actual Input Value": locator.input_value()
            }
            Reporter.log_sub_step("Verify the textbox's value after input", step_params=d2)
            if not input_value.strip() == locator.input_value().strip():
                flag = False
                Reporter.log_sub_step("Input to textbox failed")
            locator.fill("")
        assert flag, "One or more assertions failed"

    @staticmethod
    def verify_dropdown(dropdown: SingleSelectDropdown | MultiSelectDropdown, default_selected: str = None,
                        expected_options: list = None, search_str: str = None):
        """
        Method to add basic verifications for a given dropdown element
        :param dropdown:
        :param default_selected:
        :param expected_options:
        :param search_str:
        :return:
        """
        args = inspect.getframeinfo(inspect.getouterframes(inspect.currentframe())[1][0]).code_context[0].strip()
        variable_name = args[args.find('(') + 1:-1].split(',')[0].split(".")[-1]
        variable_name = " ".join(variable_name.split('_'))
        Reporter.log_step(f"Verification for {variable_name}")
        dropdown.self_object.wait_for(state="visible")
        flag = True
        if default_selected:
            d1 = {
                "Expected Default Value": default_selected,
                "Actual Default Value": dropdown.get_currently_chosen_option_text()
            }
            Reporter.log_sub_step(f"Verify dropdown default value", step_params=d1)

            if dropdown.get_currently_chosen_option_text() != default_selected:
                flag = False
        if expected_options:
            options = dropdown.get_all_options()
            d2 = {
                "Expected Options": expected_options,
                "Actual Options": options
            }
            Reporter.log_sub_step("Verify expected options in the dropdown", step_params=d2)
            flag = True
            for item in expected_options:
                if item not in options:
                    flag = False
            if not flag:
                Reporter.log_sub_step("Mismatch in expected & actual dropdown elements")
        if search_str:
            default = dropdown.get_currently_chosen_option_text()
            dropdown.select_option(search_str, True)
            TestBase.get_page().wait_for_load_state("domcontentloaded")
            selected = dropdown.get_currently_chosen_option_text()
            d3 = {
                "Expected Selected Option should contain": search_str,
                "Actual Selected Option contains": selected
            }
            Reporter.log_sub_step("Verify selected options", step_params=d3)
            if search_str not in selected:
                flag = False
                Reporter.log_sub_step("Expected value was not selected")
            dropdown.select_option(default, True)
        assert flag, "One or more assertions failed"

    @staticmethod
    def verify_table_headers(page_table: SpearlineTable, expected_values: list):
        """
        Method to add basic verifications for a table headers
        :param page_table:
        :param expected_values:
        :return:
        """
        actual_values = page_table.get_header_row().inner_text()
        actual_headers = actual_values.split("\t")
        Reporter.log_step(f"Verification for table headers", step_params={"Expected Headers": expected_values,
                                                                          "Actual Header": actual_headers})
        assert actual_headers == expected_values, "Mismatch in table headers"

    @staticmethod
    def verify_row_content(actual_values: list, expected_values: list):
        """
        Method to add basic verifications for a row content
        :param actual_values:
        :param expected_values:
        :return:
        """
        d1 = {
            "Expected Row Content": expected_values,
            "Actual Row Content": actual_values
        }
        Reporter.log_sub_step("Verify Row Content", step_params=d1)
        for index in range(len(expected_values)):
            if expected_values[index] != actual_values[index].strip():
                return index

    @staticmethod
    def verify_page_tabs(page_tab: Locator, expected_values: list):
        """
        Method to add verifications for page tabs
        :param page_tab:
        :param expected_values:
        :return:
        """
        header_tabs = page_tab.element_handles()
        headers = [header.text_content() for header in header_tabs]
        d1 = {
            "Expected Page Tab Content": expected_values,
            "Actual Page Tab Content": headers
        }
        Reporter.log_sub_step("Verify Page Tabs", step_params=d1)
        assert headers == expected_values, "Mismatch in page tab headers"

    @staticmethod
    def filter_data_and_verify(table_locator: SpearlineTable, filter_locator: Locator | SingleSelectDropdown,
                               filter_str: str, expected_rows: int, expected_data: list = None):
        """
        Method to filter data in table and verify expected number of rows
        """
        headers = table_locator.get_header_row().inner_text().split("\t")
        if isinstance(filter_locator, SingleSelectDropdown):
            filter_locator.select_option(filter_str)
        elif isinstance(filter_locator, Locator):
            filter_locator.fill(filter_str)
            filter_locator.press("Enter")
        table_locator.wait_for_row_count(expected_rows)
        assert table_locator.get_row_count() == expected_rows, "Mismatch in actual & expected row count"
        if expected_data:
            for row_num in range(expected_rows):
                actual_row = table_locator.get_data_row(row_num).inner_text().split("\t")
                row_num = VerifyUtils.verify_row_content(actual_row, expected_data)
                if row_num is not None:
                    raise AssertionError(f"Mismatch in {headers[row_num]} row.\nActual row: {actual_row}\
                        \nExpected row: {expected_data}")

    @staticmethod
    def verify_response_keys(api_response: dict, expected_keys: str | list[str], verify_message: str = "") -> None:
        """
        Checks if the expected keys are present in the response body. The Response can have more keys.
        The check is case insensitive
        :param api_response:
        :param expected_keys:
        :param verify_message:
        :return:
        """
        args = inspect.getframeinfo(inspect.getouterframes(inspect.currentframe())[1][0]).code_context[0].strip()
        variable_name = args[args.find('(') + 1:-1].split(',')[0].split(".")[0]
        variable_name = " ".join(variable_name.split('_'))

        actual_keys = [str(actual_key).lower() for actual_key in dict(api_response).keys()]

        flag = True
        if isinstance(expected_keys, str):
            d = {
                "expected key": expected_keys.lower(),
                "actual key/s": actual_keys,
                "missing": ""
            }
            if expected_keys.lower() not in actual_keys:
                flag = False
                d["missing"] = f"[{expected_keys}] was not found in actual list of keys"
        else:
            d = {
                "expected key": expected_keys,
                "actual key/s": actual_keys,
                "missing": ""
            }
            keys_not_found = []
            for expected_key in expected_keys:
                if expected_key.lower() not in actual_keys:
                    keys_not_found.append(expected_key)
                    flag = False
            d["missing"] = keys_not_found

        if verify_message == "":
            verify_message = f"Verify expected keys are present in [{variable_name}] response"

        Reporter.log_step(verify_message, step_params=d)
        assert flag, "One or more Expected key/s were not present in Actual Response"

    @staticmethod
    def verify_response_size(response_object: dict | list, expected_length: int, verify_message: str = "") -> None:
        """
        Verify the length of an object specially dict or list
        :param response_object: An iterable object whose key size you want to verify
        :param expected_length: number of expected keys / items
        :param verify_message: Message that you want to print during verification
        :return:
        """
        args = inspect.getframeinfo(inspect.getouterframes(inspect.currentframe())[1][0]).code_context[0].strip()
        variable_name = args[args.find('(') + 1:-1].split(',')[0].split(".")[0]
        variable_name = " ".join(variable_name.split('_'))

        d = {
            "expected length": expected_length,
            "actual length": len(response_object)
        }

        if verify_message == "":
            verify_message = f"Verify length of keys in [{variable_name}] is [{expected_length}]"

        Reporter.log_step(verify_message, step_params=d)
        assert len(response_object) == expected_length, "item count mismatch"

    @staticmethod
    def verify_response(api_response: dict, expected_response: dict, verify_message: str = "") -> None:
        """
        Verify the expected response items matches the actual response body
        :param api_response:
        :param expected_response:
        :param verify_message:
        :return:
        """
        args = inspect.getframeinfo(inspect.getouterframes(inspect.currentframe())[1][0]).code_context[0].strip()
        variable_name = args[args.find('(') + 1:-1].split(',')[0].split(".")[0]
        variable_name = " ".join(variable_name.split('_'))

        flag = True
        d = {
            "expected response": expected_response,
            "actual response": api_response,
            "mismatch": ""
        }
        mismatch_keys = []
        for expected_key in expected_response.keys():
            if api_response.get(expected_key) is None and api_response.get(expected_key) == expected_response.get(
                    expected_key):
                flag = False
                mismatch_keys.append(expected_key)
        d["mismatch"] = mismatch_keys

        if verify_message == "":
            verify_message = f"Verify actual response of [{variable_name}] contains Expected Response"

        Reporter.log_step(verify_message, step_params=d)
        assert flag, "Expected response does not match with Actual response"

    @staticmethod
    def verify_list_contains_expected_items(actual_list: list, expected_items: list | str | int | float,
                                            verify_message: str = "") -> None:
        """
        Verify if the expected item|items are present in the actual list
        :param actual_list:
        :param expected_items:
        :param verify_message:
        :return:
        """
        args = inspect.getframeinfo(inspect.getouterframes(inspect.currentframe())[1][0]).code_context[0].strip()
        variable_name = args[args.find('(') + 1:-1].split(',')[0].split(".")[0]
        variable_name = " ".join(variable_name.split('_'))

        flag = True
        d = {
            "expected": expected_items,
            "actual": actual_list,
            "missing": ""
        }
        missing_items = []
        if isinstance(expected_items, list):
            for expected_item in expected_items:
                if expected_item not in actual_list:
                    flag = False
                    missing_items.append(expected_item)
            d["missing"] = missing_items
        else:
            if expected_items not in actual_list:
                flag = False
            d["missing"] = missing_items

        if verify_message == "":
            verify_message = f"Verify actual items of [{variable_name}] contains Expected items"

        Reporter.log_step(verify_message, step_params=d)
        assert flag, "Expected items are not present in Actual items in list"


class StringUtils:
    """
    Contains common support methods
    """

    @staticmethod
    def generate_random_alphanumeric(size: int):
        """
        Returns randomly generated alphanumeric string
        """
        return ''.join(random.choices(string.ascii_letters + string.digits, k=size))


class DateUtils:
    """
    Support methods for Date
    """

    @staticmethod
    def date_add_days(day_count: int):
        """
        Returns future date & time in YYYY-MM-DD format
        """
        return datetime.date.today() + datetime.timedelta(days=day_count)

    @staticmethod
    def get_timestamp():
        """
        Returns current epoch
        """
        return str(int(time.time()))

    @staticmethod
    def get_weekday():
        """
        Returns weekday in string
        """
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        return days[datetime.date.today().weekday()]


class WaitUtils:
    """
    Custom Wait helpers on PlayWright objects
    """

    @staticmethod
    def wait_for_attribute_to_have(element: Locator, attribute_name: str, attribute_value: str,
                                   timeout_seconds: int = 15) -> None:
        """
        Waits till the given conditions is satisfied
        :param element: The Element on which the condition is to be checked
        :param attribute_name: The Attribute on which the condition is required
        :param attribute_value: The expected value of the attribute
        :param timeout_seconds: Will resume script after this amount of time if condition is not satisfied
        :return: None
        """
        count = 1
        while attribute_value not in element.get_attribute(attribute_name) and count <= timeout_seconds:
            time.sleep(1)
            count += 1

    @staticmethod
    def wait_for_attribute_not_to_have(element: Locator, attribute_name: str, attribute_value: str,
                                       timeout_seconds: int = 15) -> None:
        """
        Waits till the given conditions is satisfied
        :param element: The Element on which the condition is to be checked
        :param attribute_name: The Attribute on which the condition is required
        :param attribute_value: The expected value of the attribute
        :param timeout_seconds: Will resume script after this amount of time if condition is not satisfied
        :return: None
        """
        count = 1
        while attribute_value in element.get_attribute(attribute_name) and count <= timeout_seconds:
            time.sleep(1)
            count += 1

    @staticmethod
    def wait_for_element_to_enable(element: Locator, timeout_seconds: int = 15) -> None:
        """
        Waits till an element is enabled
        :param element: The Element on which the condition is to be checked
        :param timeout_seconds: Will resume script after this amount of time if condition is not satisfied
        :return: None
        """
        count = 1
        while element.is_disabled and count <= timeout_seconds:
            time.sleep(1)
            count += 1

    @staticmethod
    def wait_for_element_to_disable(element: Locator, timeout_seconds: int = 15) -> None:
        """
        Waits till an element is disabled
        :param element: The Element on which the condition is to be checked
        :param timeout_seconds: Will resume script after this amount of time if condition is not satisfied
        :return: None
        """
        count = 1
        while element.is_enabled and count <= timeout_seconds:
            time.sleep(1)
            count += 1

    @staticmethod
    def wait_for_element_to_have_text(element: Locator, expected_text: str, timeout_seconds: int = 15) -> None:
        """
        Waits till an element to have expected text
        :param element: The Element on which the condition is to be checked
        :param expected_text: The expected text
        :param timeout_seconds: Will resume script after this amount of time if condition is not satisfied
        :return: None
        """
        count = 1
        while expected_text not in element.input_value() and count <= timeout_seconds:
            time.sleep(1)
            count += 1

    @staticmethod
    def wait_for_element_not_to_have_text(element: Locator, expected_text: str, timeout_seconds: int = 15) -> None:
        """
        Waits till an element not to have expected text
        :param element: The Element on which the condition is to be checked
        :param expected_text: The expected text which should not be present
        :param timeout_seconds: Will resume script after this amount of time if condition is not satisfied
        :return: None
        """
        count = 1
        while expected_text in element.input_value() and count <= timeout_seconds:
            time.sleep(1)
            count += 1


class PlaywrightUtils:
    """
    Utility methods on Playwright classes like Locator
    """

    @staticmethod
    def set_text(element: Locator, value: str) -> None:
        """
        :param element:
        :param value:
        :return:
        """
        if value is not None and element.is_visible():
            element.fill(value)

    @staticmethod
    def select_text(element: SingleSelectDropdown | MultiSelectDropdown, value: str | list[str],
                    search_option: bool = False) -> None:
        """
        :param element:
        :param value:
        :param search_option:
        :return:
        """
        if value is not None and element.self_object.is_visible():
            element.select_option(value, search_option)
        TestBase.get_page().wait_for_load_state("domcontentloaded")
        TestBase.get_page().wait_for_load_state("networkidle")

    @staticmethod
    def set_checkbox(element: Locator, value: str | bool) -> None:
        """
        checks or unchecks the checkbox based on the value
        :param element:
        :param value:
        :return:
        """

        if value is not None and element.is_visible():
            if isinstance(value, str):
                if value.lower() in ["true", "on"]:
                    element.check()
                else:
                    element.uncheck()
            elif isinstance(value, bool):
                if value:
                    element.check()
                else:
                    element.uncheck()

    @staticmethod
    def hover(element: Locator) -> None:
        """
        Hovers over a given element using mouse move
        :param element: Element on which you want to hover
        :return: None
        """
        if element.is_visible():
            bounding_box = element.bounding_box()
            obj_x = bounding_box["x"]
            obj_y = bounding_box["y"]
            obj_width = bounding_box["width"]
            obj_height = bounding_box["height"]
            TestBase.get_page().mouse.move(obj_x + obj_width / 2, obj_y + obj_height / 2)

    @staticmethod
    def mouse_click(element: Locator) -> None:
        """
        Clicks over a given element using mouse
        :param element: Element on which you want to click
        :return: None
        """
        if element.is_visible():
            bounding_box = element.bounding_box()
            obj_x = bounding_box["x"]
            obj_y = bounding_box["y"]
            obj_width = bounding_box["width"]
            obj_height = bounding_box["height"]
            TestBase.get_page().mouse.click(obj_x + obj_width / 2, obj_y + obj_height / 2)

    @staticmethod
    def js_click(element: Locator) -> None:
        """
        Clicks over a given element which is hidden or
        overlapped by some other element
        :param element: Element on which you want to click
        :return: None
        """
        element.evaluate("link => link.click();")
        TestBase.get_page().wait_for_load_state("domcontentloaded")
        TestBase.get_page().wait_for_load_state("networkidle")

    @staticmethod
    def scroll() -> None:
        """
        Performs scroll till the bottom of page
        """
        for i in range(5):
            TestBase.get_page().mouse.wheel(0, 15000)
            time.sleep(0.5)
            i += 1

    @staticmethod
    def download_file(locator: Locator, file_name: str) -> None:
        """
        Download the file present on the page
        """
        flag = False
        with TestBase.get_page().expect_download() as download_info:
            locator.click(timeout=40000)
            dir_path = TestBase.get_project_root_path()
            temp_path = os.path.join(dir_path, file_name)
            download = download_info.value
            # Wait for the file to get downloaded and then resume
            Reporter.log_status(f"Download file location: {download.path()}")
            download.save_as(temp_path)
            if os.path.exists(temp_path):
                flag = True
            os.remove(temp_path)
            assert flag, f"The {file_name} file was not downloaded properly"

    @staticmethod
    def upload_file(locator: Locator, file_name: str) -> None:
        """
        Upload a the file of given file_path
        """
        # FileChooser.set_files(FileChooser, file_path)
        with TestBase.get_page().expect_file_chooser() as file_upload_info:
            locator.click(timeout=40000)
            dir_path = TestBase.get_project_root_path()
            temp_path = os.path.join(dir_path, file_name)
            file_chooser: FileChooser = file_upload_info.value
            file_chooser.set_files([temp_path])
            # Wait for the file to get downloaded and then resume
            Reporter.log_status(f"Uploaded file location: {file_name}")
    
    @staticmethod
    def count_file_records(file_name: str) -> None:
        """
        Count total number of records in a CSV file
        """
        dir_path = TestBase.get_project_root_path()
        temp_path = os.path.join(dir_path, file_name)
        count = 0
        with open(temp_path, 'r') as file:
            reader = csv.reader(file)
            # to skip the header row
            next(reader)
            for _ in reader:
                count += 1
        return count


class CustomVerifications:
    def __init__(self, actual_object: dict | list | str | int | bool | float):
        self.actual_object = actual_object

    def is_sorted_in_ascending(self, verify_msg: str = ""):
        """
        Verifies if the given list is sorted correctly in ascending order
        :param verify_msg:
        :return:
        """
        if isinstance(self.actual_object, list):
            Reporter.log_step(verify_msg, step_params=self.actual_object)
            flag = True
            if isinstance(self.actual_object[0], str):
                for index in range(1, len(self.actual_object)):
                    if self.actual_object[index].lower() < self.actual_object[index - 1].lower():
                        flag = False
                        Reporter.log_sub_step(
                            f"[{self.actual_object[index - 1]}] should come after [{self.actual_object[index]}]]")
                        break
                assert flag, "List is not sorted in ascending order"

            else:
                for index in range(1, len(self.actual_object)):
                    if self.actual_object[index] < self.actual_object[index - 1]:
                        flag = False
                        Reporter.log_sub_step(
                            f"[{self.actual_object[index - 1]}] should come after [{self.actual_object[index]}]]")
                        break
                assert flag, "List is not sorted in ascending order"
        else:
            assert False, "Cannot verify sorting on variables other than List type"

    def is_sorted_in_descending(self, verify_msg: str = ""):
        """
        Verifies if the given list is sorted correctly in ascending order
        :param verify_msg:
        :return:
        """
        if isinstance(self.actual_object, list):
            Reporter.log_step(verify_msg, step_params=self.actual_object)
            flag = True
            if isinstance(self.actual_object[0], str):
                for index in range(1, len(self.actual_object)):
                    if self.actual_object[index].lower() > self.actual_object[index - 1].lower():
                        flag = False
                        Reporter.log_sub_step(
                            f"[{self.actual_object[index - 1]}] should come after [{self.actual_object[index]}]]")
                        break
                assert flag, "List is not sorted in descending order"
            else:
                for index in range(1, len(self.actual_object)):
                    if self.actual_object[index] > self.actual_object[index - 1]:
                        flag = False
                        Reporter.log_sub_step(
                            f"[{self.actual_object[index - 1]}] should come after [{self.actual_object[index]}]]")
                        break
                assert flag, "List is not sorted in descending order"
        else:
            assert False, "Cannot verify sorting on variables other than List type"

    def is_not_sorted_in_ascending(self, verify_msg: str = ""):
        """
        Verifies if the given list is not sorted in ascending order
        :param verify_msg:
        :return:
        """
        if isinstance(self.actual_object, list):
            Reporter.log_step(verify_msg, step_params=self.actual_object)
            flag = False
            if isinstance(self.actual_object[0], str):
                for index in range(1, len(self.actual_object)):
                    if self.actual_object[index].lower() < self.actual_object[index - 1].lower():
                        flag = True
                        Reporter.log_sub_step(
                            f"[{self.actual_object[index - 1]}] should come after [{self.actual_object[index]}]]")
                        break
                assert flag, "List is sorted in ascending order"

            else:
                for index in range(1, len(self.actual_object)):
                    if self.actual_object[index] < self.actual_object[index - 1]:
                        flag = True
                        Reporter.log_sub_step(
                            f"[{self.actual_object[index - 1]}] should come after [{self.actual_object[index]}]]")
                        break
                assert flag, "List is sorted in ascending order"
        else:
            assert False, "Cannot verify sorting on variables other than List type"

    def has_keys(self, expected_keys: str | list[str], verify_message: str = "") -> None:
        """
        Checks if the expected keys are exactly present in the dict object.
        If the actual object has more keys this verification fails. For such cases try the contains_keys verification

        The check is case insensitive
        :param expected_keys: can be a single string or a list of strings
        :param verify_message: Verification message that you want to show in the Allure Report
        :return:
        """
        if isinstance(self.actual_object, dict):
            actual_keys = [str(actual_key).lower() for actual_key in dict(self.actual_object).keys()]

            flag = True
            if isinstance(expected_keys, str):
                d = {
                    "expected key": expected_keys.lower(),
                    "actual key": actual_keys
                }
                if expected_keys.lower() != actual_keys[0] or len(actual_keys) != 1:
                    flag = False
            else:
                d = {
                    "expected keys": expected_keys,
                    "actual keys": actual_keys,
                    "missing": "",
                    "message": ""
                }
                keys_not_found = []
                for expected_key in expected_keys:
                    if expected_key.lower() not in actual_keys:
                        keys_not_found.append(expected_key)
                        flag = False
                d["missing"] = keys_not_found
                message = ""
                if len(expected_keys) != len(actual_keys):
                    flag = False
                    message = f"Expected Keys were [{len(expected_keys)}] but Actual Keys were [{len(actual_keys)}]"
                d["message"] = message

            Reporter.log_step(verify_message, step_params=d)
            assert flag, "Failure in Expected and Actual key/s"

        else:
            assert False, "Cannot verify presence of Keys on variables other than Dict type"

    def contains_keys(self, expected_keys: str | list[str], verify_message: str = "") -> None:
        """
        Checks if the expected keys is present in the actual object. The actual object can have more keys

        The check is case insensitive
        :param expected_keys: can be a single string or a list of strings
        :param verify_message: Verification message that you want to show in the Allure Report
        :return:
        """
        if isinstance(self.actual_object, dict):
            actual_keys = [str(actual_key).lower() for actual_key in dict(self.actual_object).keys()]

            flag = True
            if isinstance(expected_keys, str):
                d = {
                    "expected key": expected_keys.lower(),
                    "actual key/s": actual_keys,
                    "missing": ""
                }
                if expected_keys.lower() not in actual_keys:
                    flag = False
                    d["missing"] = expected_keys
            else:
                d = {
                    "expected key": expected_keys,
                    "actual key/s": actual_keys,
                    "missing": ""
                }
                keys_not_found = []
                for expected_key in expected_keys:
                    if expected_key.lower() not in actual_keys:
                        keys_not_found.append(expected_key)
                        flag = False
                d["missing"] = keys_not_found

            Reporter.log_step(verify_message, step_params=d)
            assert flag, "One or more Expected key/s were not present in Actual Response"

        else:
            assert False, "Cannot verify presence of Keys on variables other than Dict type"

    def does_not_contain_keys(self, expected_keys: str | list[str], verify_message: str = "") -> None:
        """
        Checks if the expected keys is/are NOT present in the actual object. The actual object can have more keys

        The check is case insensitive
        :param expected_keys: can be a single string or a list of strings
        :param verify_message: Verification message that you want to show in the Allure Report
        :return:
        """
        if isinstance(self.actual_object, dict):
            actual_keys = [str(actual_key).lower() for actual_key in dict(self.actual_object).keys()]

            flag = True
            if isinstance(expected_keys, str):
                d = {
                    "expected key": expected_keys.lower(),
                    "actual key/s": actual_keys,
                    "present": ""
                }
                if expected_keys.lower() in actual_keys:
                    flag = False
                    d["present"] = expected_keys
            else:
                d = {
                    "expected key": expected_keys,
                    "actual key/s": actual_keys,
                    "present": ""
                }
                keys_found = []
                for expected_key in expected_keys:
                    if expected_key.lower() in actual_keys:
                        keys_found.append(expected_key)
                        flag = False
                d["present"] = keys_found

            Reporter.log_step(verify_message, step_params=d)
            assert flag, "One or more Expected key/s were present in Actual Response"

        else:
            assert False, "Cannot verify presence of Keys on variables other than Dict type"

    def has_no_of_items_equal_to(self, expected_length: int, verify_message: str = ""):
        """
        Verify the length of an object specially dict or list
        :param expected_length: number of expected keys / items
        :param verify_message: Message that you want to print during verification
        :return:
        """

        if isinstance(self.actual_object, list) or isinstance(self.actual_object, dict):
            d = {
                "expected no of items": expected_length,
                "actual no of items": len(self.actual_object)
            }
            Reporter.log_step(verify_message, step_params=d)
            assert len(self.actual_object) == expected_length, "item count mismatch"
        else:
            assert False, "Cannot verify no of items on variables other than Dict or List type"

    def has_no_of_items_more_than(self, expected_length: int, verify_message: str = ""):
        """
        Verify the length of an object specially dict or list is more than expected
        :param expected_length: number of expected keys / items
        :param verify_message: Message that you want to print during verification
        :return:
        """

        if isinstance(self.actual_object, list) or isinstance(self.actual_object, dict):
            d = {
                "expected no of items": f"more than [{expected_length}]",
                "actual no of items": len(self.actual_object)
            }
            Reporter.log_step(verify_message, step_params=d)
            assert len(self.actual_object) > expected_length, "item count mismatch"
        else:
            assert False, "Cannot verify no of items on variables other than Dict or List type"

    def has_no_of_items_less_than(self, expected_length: int, verify_message: str = ""):
        """
        Verify the length of an object specially dict or list is less than expected
        :param expected_length: number of expected keys / items
        :param verify_message: Message that you want to print during verification
        :return:
        """

        if isinstance(self.actual_object, list) or isinstance(self.actual_object, dict):
            d = {
                "expected no of items": f"less than [{expected_length}]",
                "actual no of items": len(self.actual_object)
            }
            Reporter.log_step(verify_message, step_params=d)
            assert len(self.actual_object) < expected_length, "item count mismatch"
        else:
            assert False, "Cannot verify no of items on variables other than Dict or List type"

    def has_items(self, expected_items: dict | list, verify_message: str = "") -> None:
        """
        Verify the expected items is/are equals to the items in actual object.
        The actual object cannot have more items. For such cases refer contains_items
        :param expected_items:
        :param verify_message:
        :return:
        """
        if isinstance(self.actual_object, dict) and isinstance(expected_items, dict):
            flag = True
            d = {
                "expected items": expected_items,
                "actual items": self.actual_object,
                "mismatch": "",
                "message": ""
            }
            mismatch_keys = []
            for expected_key in expected_items.keys():
                if self.actual_object.get(expected_key) is None or \
                        self.actual_object.get(expected_key) != expected_items.get(expected_key):
                    flag = False
                    mismatch_keys.append(expected_key)
            d["mismatch"] = mismatch_keys

            message = ""
            if len(expected_items) != len(self.actual_object):
                flag = False
                message = f"Expected Items were [{len(expected_items)}] but Actual Items were [{len(self.actual_object)}]"
            d["message"] = message

            Reporter.log_step(verify_message, step_params=d)
            assert flag, "Expected items is/are not present in Actual object"

        elif isinstance(self.actual_object, list) and isinstance(expected_items, list):
            flag = True
            d = {
                "expected items": expected_items,
                "actual items": self.actual_object,
                "mismatch": ""
            }
            mismatch_keys = []
            for expected_item in expected_items:
                if expected_item not in self.actual_object:
                    flag = False
                    mismatch_keys.append(expected_item)
            d["mismatch"] = mismatch_keys

            message = ""
            if len(expected_items) != len(self.actual_object):
                flag = False
                message = f"Expected Items were [{len(expected_items)}] but Actual Items were [{len(self.actual_object)}]"
            d["message"] = message

            Reporter.log_step(verify_message, step_params=d)
            assert flag, "Expected items is/are not present in Actual object"

        else:
            assert False, "Cannot verify presence of Items on variables other than Dict or List type"

    def contains_items(self, expected_items: dict | list, verify_message: str = "") -> None:
        """
        Verify the expected items is/are present in the actual object. The actual object can have more items
        :param expected_items:
        :param verify_message:
        :return:
        """
        if isinstance(self.actual_object, dict) and isinstance(expected_items, dict):
            flag = True
            d = {
                "expected items": expected_items,
                "actual items": self.actual_object,
                "mismatch": ""
            }
            mismatch_keys = []
            for expected_key in expected_items.keys():
                if self.actual_object.get(expected_key) is None or \
                        self.actual_object.get(expected_key) != expected_items.get(expected_key):
                    flag = False
                    mismatch_keys.append(expected_key)
            d["mismatch"] = mismatch_keys

            Reporter.log_step(verify_message, step_params=d)
            assert flag, "Expected items is/are not present in Actual object"

        elif isinstance(self.actual_object, list) and isinstance(expected_items, list):
            flag = True
            d = {
                "expected items": expected_items,
                "actual items": self.actual_object,
                "mismatch": ""
            }
            mismatch_keys = []
            for expected_item in expected_items:
                if expected_item not in self.actual_object:
                    flag = False
                    mismatch_keys.append(expected_item)
            d["mismatch"] = mismatch_keys

            Reporter.log_step(verify_message, step_params=d)
            assert flag, "Expected items is/are not present in Actual object"

        else:
            assert False, "Cannot verify presence of Items on variables other than Dict or List type"

    def does_not_contains_items(self, expected_items: dict | list, verify_message: str = ""):
        """
        Verify the expected items is/are NOT present in the actual object. The actual object can have more items
        :param expected_items:
        :param verify_message:
        :return:
        """
        if isinstance(self.actual_object, dict) and isinstance(expected_items, dict):
            flag = True
            d = {
                "expected items": expected_items,
                "actual items": self.actual_object,
                "present": ""
            }
            mismatch_keys = []
            for expected_key in expected_items.keys():
                if self.actual_object.get(expected_key) is not None or \
                        self.actual_object.get(expected_key) == expected_items.get(expected_key):
                    flag = False
                    mismatch_keys.append(expected_key)
            d["present"] = mismatch_keys

            Reporter.log_step(verify_message, step_params=d)
            assert flag, "Expected items is/are present in Actual object"

        elif isinstance(self.actual_object, list) and isinstance(expected_items, list):
            flag = True
            d = {
                "expected items": expected_items,
                "actual items": self.actual_object,
                "present": ""
            }
            mismatch_keys = []
            for expected_item in expected_items:
                if expected_item in self.actual_object:
                    flag = False
                    mismatch_keys.append(expected_item)
            d["present"] = mismatch_keys

            Reporter.log_step(verify_message, step_params=d)
            assert flag, "Expected items is/are present in Actual object"

        else:
            assert False, "Cannot verify presence of Items on variables other than Dict or List type"

    def contains_items_greater_than(self, expected_item: str | int | float, verify_message: str = "") -> None:
        """
        Checks whether all items in the list is greater than a particular expected item
        :param expected_item:
        :param verify_message:
        :return:
        """
        if isinstance(self.actual_object, list):
            flag = True
            d = {
                "expected greater than": expected_item,
                "actual items": self.actual_object,
                "message": ""
            }

            for item in self.actual_object:
                if item <= expected_item:
                    flag = False
                    d["message"] = f"[{item} is not greater than [{expected_item}]]"
                    break

            Reporter.log_step(verify_message, step_params=d)
            assert flag, "Actual items are not greater than Expected Item"

        else:
            assert False, "Cannot verify 'items are greater than' on variables other than List type"

    def contains_items_greater_than_or_equal_to(self, expected_item: str | int | float,
                                                verify_message: str = "") -> None:
        """
        Checks whether all items in the list is greater than or equal to a particular expected item
        :param expected_item:
        :param verify_message:
        :return:
        """
        if isinstance(self.actual_object, list):
            flag = True
            d = {
                "expected greater than or equal to": expected_item,
                "actual items": self.actual_object,
                "message": ""
            }

            for item in self.actual_object:
                if item < expected_item:
                    flag = False
                    d["message"] = f"[{item} is not greater than or equal [{expected_item}]]"
                    break

            Reporter.log_step(verify_message, step_params=d)
            assert flag, "Actual items are not greater than or Equal to Expected Item"

        else:
            assert False, "Cannot verify 'items are greater than or equals' on variables other than List type"

    def contains_items_less_than(self, expected_item: str | int | float, verify_message: str = "") -> None:
        """
        Checks whether all items in the list is less than a particular expected item
        :param expected_item:
        :param verify_message:
        :return:
        """
        if isinstance(self.actual_object, list):
            flag = True
            d = {
                "expected less than": expected_item,
                "actual items": self.actual_object,
                "message": ""
            }

            for item in self.actual_object:
                if item >= expected_item:
                    flag = False
                    d["message"] = f"[{item} is not less than [{expected_item}]]"
                    break

            Reporter.log_step(verify_message, step_params=d)
            assert flag, "Actual items are not less than Expected Item"

        else:
            assert False, "Cannot verify 'items are less than' on variables other than List type"

    def contains_items_less_than_or_equal_to(self, expected_item: str | int | float, verify_message: str = "") -> None:
        """
        Checks whether all items in the list is less than or equals to a particular expected item
        :param expected_item:
        :param verify_message:
        :return:
        """
        if isinstance(self.actual_object, list):
            flag = True
            d = {
                "expected less than or equal to": expected_item,
                "actual items": self.actual_object,
                "message": ""
            }

            for item in self.actual_object:
                if item > expected_item:
                    flag = False
                    d["message"] = f"[{item} is not less than or equal[{expected_item}]]"
                    break

            Reporter.log_step(verify_message, step_params=d)
            assert flag, "Actual items are not less or equal to Expected Item"

        else:
            assert False, "Cannot verify 'items are less than or equal' on variables other than List type"

    def contains_items_between(self, expected_item_lower: str | int | float,
                               expected_item_greater: str | int | float,
                               verify_message: str = "") -> None:
        """
        Checks whether all items in the list is between the expected items
        :param expected_item_lower:
        :param expected_item_greater:
        :param verify_message:
        :return:
        """
        if isinstance(self.actual_object, list):
            flag = True
            d = {
                "expected range": f"greater than [{expected_item_lower}] and less than [{expected_item_greater}]",
                "actual items": self.actual_object,
                "message": ""
            }

            for item in self.actual_object:
                if item < expected_item_lower or item > expected_item_greater:
                    flag = False
                    d["message"] = f"[{item}] is not between [{expected_item_lower}] and [{expected_item_greater}]"
                    break

            Reporter.log_step(verify_message, step_params=d)
            assert flag, "Actual items are not between Expected Items"

        else:
            assert False, "Cannot verify 'items are less than or equal' on variables other than List type"

    def contains_items_like(self, expected_item: str, verify_message: str = "", ignore_case: bool = True) -> None:
        """
        Checks whether all items in the list is matching the regex pattern for the expected item
        :param expected_item:
        :param verify_message:
        :param ignore_case:
        :return:
        """
        if isinstance(self.actual_object, list):
            flag = True
            d = {
                "expected range": f"like [{expected_item}]",
                "actual items": self.actual_object,
                "message": ""
            }
            expected_item = expected_item.replace("%", ".*").replace("_", ".")
            if ignore_case:
                expected_item = re.compile(expected_item, re.IGNORECASE)
            else:
                expected_item = re.compile(expected_item)
            for item in self.actual_object:
                if re.search(expected_item, item) is None:
                    flag = False
                    d["message"] = f"[{item}] is not like [{expected_item}]"
                    break

            Reporter.log_step(verify_message, step_params=d)
            assert flag, "Actual items are not Like Expected Items"

        else:
            assert False, "Cannot verify 'items are like' on variables other than List type"

    def contains_items_not_like(self, expected_item: str, verify_message: str = "", ignore_case: bool = True) -> None:
        """
        Checks whether all items in the list is matching the regex pattern for the expected item
        :param expected_item:
        :param verify_message:
        :param ignore_case:
        :return:
        """
        if isinstance(self.actual_object, list):
            flag = True
            d = {
                "expected range": f"like [{expected_item}]",
                "actual items": self.actual_object,
                "message": ""
            }
            expected_item = expected_item.replace("%", ".*").replace("_", ".")
            if ignore_case:
                expected_item = re.compile(expected_item, re.IGNORECASE)
            else:
                expected_item = re.compile(expected_item)
            for item in self.actual_object:
                if re.search(expected_item, item) is not None:
                    flag = False
                    d["message"] = f"[{item}] is like [{expected_item}]"
                    break

            Reporter.log_step(verify_message, step_params=d)
            assert flag, "Actual items are not Like Expected Items"

        else:
            assert False, "Cannot verify 'items are like' on variables other than List type"


class CustomCheckers:
    """
    A Class that returns True / False only. Does not assert
    """
    def __init__(self, actual_object: str | int | bool | float):
        self.actual_object = actual_object

    def is_equal_to(self, expected_object: str | int | bool | float | list | dict, message = ""):
        """
        Checks if 2 objects are equal and Logs information in Allure Report. Does not assert
        :param expected_object:
        :param message:
        :return: True / False
        """
        temp = {
            "Actual": str(self.actual_object),
            "Expected ": str(expected_object)
        }
        Reporter.log_step(message, step_params=temp)
        if self.actual_object != expected_object:
            return False
        return True

    def contains(self, expected_object: str | list | dict, message = ""):
        """
        Checks if the expected value is present in the actual object and logs information in Allure. Does not assert
        :param expected_object:
        :param message:
        :return:
        """
        temp = {
            "Actual": str(self.actual_object),
            "Expected ": str(expected_object)
        }
        Reporter.log_step(message, step_params=temp)
        if expected_object.lower() not in self.actual_object.lower():
            return False
        return True


def verify(argument: dict | list):
    return CustomVerifications(argument)


def check(argument: str | int | float | list | dict):
    return CustomCheckers(argument)


class MarshalUtils:
    """
    Class utils used for Marshalling and Unmarshalling instance
    """

    @staticmethod
    def remove_empty_items(obj: dict) -> dict:
        """
        Removes items from dictionary that is None
        :param obj:
        :return: dict
        """
        temp = {}
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, dict):
                    temp[k] = MarshalUtils.remove_empty_items(obj[k])
                elif v is not None:
                    temp[k] = v
            return temp
        return None
