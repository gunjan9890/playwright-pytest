import time

from spearline_qa_src.lib.test_base import TestBase

url = "https://the-internet.herokuapp.com/jqueryui/menu"

TestBase.get_page().goto(url)


#disabled link check
disabled_link = TestBase.get_page().locator("xpath=//a[text()='Disabled']")
print("Link Enabled ? : ", disabled_link.is_enabled())

#enabled link
enabled_lnk = TestBase.get_page().locator("xpath=//a[text()='Enabled']")
TestBase.get_page().mouse.move(enabled_lnk.bounding_box()['x'] + 5, enabled_lnk.bounding_box()['y'] + 5)
time.sleep(1)

#Downlaods  link
downloads_lnk = TestBase.get_page().locator("xpath=//a[text()='Downloads']")
TestBase.get_page().mouse.move(downloads_lnk.bounding_box()['x'] + 5, downloads_lnk.bounding_box()['y'] + 5)


hidden_link = TestBase.get_page().locator("xpath=//a[text()='PDF']")
# first argument to the Lambda represents the current Locator's corresponding element on UI
print(hidden_link.evaluate("link => link.innerText"))



# using javascript to click on a specific Locator (which can be hidden)
with TestBase.get_page().expect_download() as download_file:
    hidden_link.evaluate("link => link.click();")
    download_file.value.save_as("hidden_jquery_file.pdf")

# hidden_link.click(force=True)

time.sleep(10)