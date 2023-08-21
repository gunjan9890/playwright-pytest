import time

from spearline_qa_src.lib.test_base import TestBase

url = "https://the-internet.herokuapp.com/windows"

def handle_pop(pop):
    print(f"New Page Title {pop.title()}")

TestBase.get_page().on("popup", handle_pop)
TestBase.get_page().goto(url)


click_here = TestBase.get_page().locator("a", has_text="Click Here")

click_here.click()

with TestBase.get_page().expect_event("popup") as pop:
    click_here.click()
    new_page = pop.value
    print(new_page.locator("h3").text_content())
    new_page.close()

time.sleep(5)
# TestBase.get_page().close()
