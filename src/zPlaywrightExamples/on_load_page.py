import time

from playwright.sync_api import Page

from spearline_qa_src.lib.test_base import TestBase

url = "https://the-internet.herokuapp.com/javascript_error"

def handle_load(load: Page):
    print("page loaded")

TestBase.get_page().on("load", handle_load)
TestBase.get_page().goto(url)
time.sleep(5)
TestBase.get_page().close()
