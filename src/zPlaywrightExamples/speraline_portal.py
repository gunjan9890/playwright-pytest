
from spearline_qa_src.lib.test_base import TestBase

TestBase.get_page().goto("https://qa-staging.spearline.com/admin/user/login")
TestBase.get_page().locator("#email >> visible=true").fill("qa.service@spearline.com")
TestBase.get_page().locator("#password >> visible=true").fill("T3STp4ss!")
TestBase.get_page().locator("#log-in").click()