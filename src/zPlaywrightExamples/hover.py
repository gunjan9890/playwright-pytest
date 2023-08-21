import time
from spearline_qa_src.lib.test_base import TestBase

url = "https://the-internet.herokuapp.com/hovers"

TestBase.get_page().goto(url)
time.sleep(2)

locator1 = TestBase.get_page().locator("//div[@class='figure']").nth(0)
locator2 = TestBase.get_page().locator("//div[@class='figure']").nth(1)
locator3 = TestBase.get_page().locator("//div[@class='figure']").nth(2)

TestBase.get_page().mouse.move(locator1.bounding_box()["x"], locator1.bounding_box()["y"])
time.sleep(2)

TestBase.get_page().mouse.move(locator2.bounding_box()["x"], locator2.bounding_box()["y"])
time.sleep(2)

TestBase.get_page().mouse.move(locator3.bounding_box()["x"], locator3.bounding_box()["y"])
time.sleep(2)