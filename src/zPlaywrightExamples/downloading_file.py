import time

from playwright.sync_api import Download

from spearline_qa_src.lib.test_base import TestBase

url = "https://the-internet.herokuapp.com/download"

def handle_download(download: Download):
    time.sleep(1)
    print(f"The file was downloaded at : {download.path()}")
    time.sleep(1)

TestBase.get_page().goto(url)
download_link = TestBase.get_page().locator("xpath=//a[text()='example.json']")


time.sleep(1)

with TestBase.get_page().expect_download() as download_info:
    download_link.click()
    download_info.value.save_as("theFileYouWant.json")

download_details = download_info.value
print(download_details.path())
# download_details.delete()

time.sleep(1)

zip_download_link = TestBase.get_page().locator("xpath=//a[text()='plain_root_multiple_zips_downloaded.zip']")

with TestBase.get_page().expect_download() as download_info:
    zip_download_link.click()
    download_info.value.cancel()
    # download_info.value.save_as("theZipDownload.zip")


download_details = download_info.value
# print(download_details.path())
time.sleep(1)


TestBase.get_page().close()