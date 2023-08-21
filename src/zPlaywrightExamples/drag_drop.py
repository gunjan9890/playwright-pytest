import time

from spearline_qa_src.lib.test_base import TestBase

url = "https://the-internet.herokuapp.com/drag_and_drop"
TestBase.get_page().goto(url)
time.sleep(1)
sec_a = TestBase.get_page().locator("xpath=//div[@id='column-a']")
sec_b = TestBase.get_page().locator("xpath=//div[@id='column-b']")

sec_a.drag_to(sec_b)
time.sleep(1)