import time

from spearline_qa_src.lib.test_base import TestBase


#the usual way of authentication works
#the URL should be "https://<username>:<password>@<url-without-https>"

TestBase.get_page().goto("https://admin:admin@the-internet.herokuapp.com/digest_auth")
time.sleep(2)

TestBase.get_page().goto("https://admin:admin@the-internet.herokuapp.com/basic_auth")
time.sleep(2)
