"""
This Module takes care of Currently running Tests, Modules & Session
"""
from _pytest.fixtures import FixtureRequest
from allure_commons._allure import StepContext


class TestListener:
    """
    Stores imformation of currently executing Tests, Modules, Sessions
    """
    current_allure_test_step: StepContext = None
    is_current_allure_step_open: bool = False
    current_test_case_request: FixtureRequest = None
    current_test_module_request: FixtureRequest = None
    current_test_session_request: FixtureRequest = None

    current_reporter_node: FixtureRequest = None

    current_step_counter: int = 0
    total_steps: int = 0
    pass_counter: int = 0
    fail_counter: int = 0
    skip_counter: int = 0

    @staticmethod
    def get_step_counter():
        """
        returns the current step counter
        :return:
        """
        return TestListener.current_step_counter

    @staticmethod
    def close_current_allure_step():
        """
        closes the current allure step
        :return:
        """
        TestListener.current_allure_test_step.__exit__(None, None, None)
        TestListener.is_current_allure_step_open = False
