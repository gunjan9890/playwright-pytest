import time

from spearline_qa_src.lib.test_base import TestBase

url = "https://the-internet.herokuapp.com/floating_menu"

TestBase.get_page().goto(url)

footer = TestBase.get_page().locator("xpath=//div[@id='page-footer']")

print(footer.element_handle().bounding_box()['x'])
y = (footer.element_handle().bounding_box()['y'])
for i in range(10):
    TestBase.get_page().evaluate(f"window.scrollTo(0,{i*100})")
    time.sleep(1)

time.sleep(2)
TestBase.get_page().evaluate("window.scrollTo(0, 0)")
time.sleep(2)
TestBase.get_page().evaluate(f"window.scrollTo(0,{y})")

time.sleep(2)