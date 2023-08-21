import time

from spearline_qa_src.lib.test_base import TestBase

url = "https://the-internet.herokuapp.com/dropdown"

TestBase.get_page().goto(url)
time.sleep(2)
sel = TestBase.get_page().locator("xpath=//select")
sel.select_option(value="1")
print(sel.input_value())
time.sleep(2)
sel.select_option(label="Option 2")
print(sel.input_value())
time.sleep(2)
sel.select_option(index=0)
print(sel.input_value())
