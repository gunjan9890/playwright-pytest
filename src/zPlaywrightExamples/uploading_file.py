import time

from playwright.sync_api import FileChooser

from spearline_qa_src.lib.test_base import TestBase

url = "https://the-internet.herokuapp.com/upload"

def func_file_chooser(file_chooser: FileChooser):
    file_chooser.set_files(["theFileYouWant.json"])
    file_chooser.set_files("theZipDownload.zip")

TestBase.get_page().goto(url)
upload_btn = TestBase.get_page().locator("#file-upload")

TestBase.get_page().on("filechooser", func_file_chooser)

upload = TestBase.get_page().locator("#file-submit")
upload_btn.click()

time.sleep(1)
upload.click()
time.sleep(3)

TestBase.get_page().close()