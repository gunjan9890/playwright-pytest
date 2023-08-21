from playwright.sync_api import Locator
from spearline_qa_src.lib.test_base import TestBase


TestBase.get_page().goto("https://the-internet.herokuapp.com/checkboxes")
checkboxes: Locator = TestBase.get_page().locator("#checkboxes input")
print(f"Total Checkboxes : {checkboxes.count()}")
chk1 = checkboxes.nth(0)
chk2 = checkboxes.nth(1)

print(f"Checkbox 1 is Checked ? : {chk1.is_checked()}")
print(f"Checkbox 2 is Checked ? : {chk2.is_checked()}")

chk1.check()
chk2.uncheck()

print(f"Checkbox 1 is Checked ? : {chk1.is_checked()}")
print(f"Checkbox 2 is Checked ? : {chk2.is_checked()}")
