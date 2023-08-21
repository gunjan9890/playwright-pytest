from spearline_qa_src.lib.test_base import TestBase

url = "https://the-internet.herokuapp.com/disappearing_elements"
TestBase.get_page().goto(url)
# waiting till a button appears on the page
# manually keep on reloading the element

gallery = TestBase.get_page().locator("xpath=//a[text()='Gallery']")
gallery.wait_for(state="visible", timeout=60000)
gallery.click()

