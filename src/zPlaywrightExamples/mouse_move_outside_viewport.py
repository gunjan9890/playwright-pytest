import time

from spearline_qa_src.lib.test_base import TestBase

url = "https://the-internet.herokuapp.com/exit_intent"

TestBase.get_page().goto(url)
TestBase.get_page().mouse.move(50,50)
time.sleep(1)
TestBase.get_page().mouse.move(-5,-5)
time.sleep(2)