import time

from playwright.sync_api import Geolocation

from spearline_qa_src.lib.test_base import TestBase

url = "https://the-internet.herokuapp.com/geolocation"
geo = Geolocation()

context = TestBase.get_browser().new_context(geolocation={"latitude": -40, "longitude":50})
context.grant_permissions(["geolocation"])
page = context.new_page()

page.goto(url)
btn = page.locator("xpath=//button")
btn.click()

time.sleep(3)

print(page.locator("xpath=//p[@id='demo']").text_content())