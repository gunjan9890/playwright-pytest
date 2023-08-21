import time
from spearline_qa_src.lib.test_base import TestBase


TestBase.get_page().goto("https://the-internet.herokuapp.com/context_menu")
box = TestBase.get_page().locator("#hot-spot")
box.click(button='right')

# by default Playwright will Accept any dialog, so you probably wont notice
# if you want to see Dialog related action, locate handling_dialogs.py & execute that

time.sleep(2)

TestBase.get_page().close()
