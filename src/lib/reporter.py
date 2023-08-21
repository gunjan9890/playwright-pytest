"""
A module that takes care of Reporting (Console + other Reporting)
"""
import json
import logging
from enum import Enum
from typing import Any

import allure
from _pytest._io import TerminalWriter
from allure_commons._allure import StepContext

from spearline_qa_src.lib.test_base import TestBase
from spearline_qa_src.lib.test_listener import TestListener


class Reporter:
    """
    A class that handles reporting
    """

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    @staticmethod
    def log_status(msg: Any) -> None:
        """
        Logs the text to Console Writer immediately
        :param msg: String message you want to Log
        :param report_type: ReportType
        :return: None
        """
        writer: TerminalWriter = TestListener.current_reporter_node.config.get_terminal_writer()
        writer.write(str(msg))
        writer.line()

        if TestListener.is_current_allure_step_open:
            TestListener.current_allure_test_step.__exit__(None, None, None)
            TestListener.is_current_allure_step_open = False

        allure.attach(body="", name=str(msg), attachment_type=None, extension=None)
        Reporter.logger.info(str(msg))

    @staticmethod
    def log_step(step_description: str, attach_screenshot: bool = False, step_title: str = "Step ",
                 step_params: Any = None) -> None:
        """
        Creates a Test Step in the Allure Report
        :param step_description: The Description of the Step
        :param attach_screenshot:
        :param step_title: The title of the Step
        :param step_params: Additional parameters for the Step
        :return: None
        """
        TestListener.current_step_counter += 1
        if TestListener.is_current_allure_step_open:
            TestListener.current_allure_test_step.__exit__(None, None, None)
            TestListener.is_current_allure_step_open = False
        step_title += str(TestListener.current_step_counter)
        step_title += " : " + step_description

        allure_test_step: StepContext = allure.step(step_title)
        # start the allure step
        allure_test_step.__enter__()

        # set the step open
        TestListener.is_current_allure_step_open = True

        TestListener.current_allure_test_step = allure_test_step
        if isinstance(step_params, (int, str, float)):
            allure.attach(body=step_params, name="Step Parameters")
        elif isinstance(step_params, (list, dict)):
            allure.attach(body=json.dumps(step_params, indent=4), name="Step Parameters")
        if attach_screenshot:
            snap = TestBase.take_screenshot('failure', True)
            allure.attach(body=snap, name="Step Screenshot", attachment_type='png')

        # keep the allure step open in case log sub step
        # allure_test_step.__exit__(None, None, None)

    @staticmethod
    def log_sub_step(step_description: str, attach_screenshot: bool = False, step_title: str = "Step ",
                     step_params: Any = None):
        """
        Creates a Test Step in the Allure Report
        :param step_description: The Description of the Step
        :param attach_screenshot:
        :param step_title: The title of the Step
        :param step_params: Additional parameters for the Step
        :return: None
        """
        if not TestListener.is_current_allure_step_open:
            Reporter.log_step("A Step having Sub-Step")

        if isinstance(step_params, (int, str, float)):
            allure.attach(body=step_params, name=step_description)
        elif isinstance(step_params, (list, dict)):
            allure.attach(body=json.dumps(step_params, indent=4), name=step_description)
        else:
            allure.attach(body=step_description, name=step_description)
        if attach_screenshot:
            snap = TestBase.take_screenshot('failure', True)
            allure.attach(body=snap, name="Step Screenshot", attachment_type='png')
