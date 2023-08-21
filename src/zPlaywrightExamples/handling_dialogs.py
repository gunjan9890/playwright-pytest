import time

from playwright.sync_api import Dialog

from spearline_qa_src.lib.test_base import TestBase


TestBase.get_page().goto("https://the-internet.herokuapp.com/context_menu")
box = TestBase.get_page().locator("#hot-spot")
# if you right click on the above box, a new Alert is generated
# PlayWright automatically handles an Alert, but if you want the control with you,
# => Create a function, that can accept type of Handle object, and perform some operations
# just make sure, you have to Register the Event , before the Alert Happens


def handle_alert_custom(dialog: Dialog):
    print("Your Alert Message is : ", dialog.message)
    # waiting for 2 seconds so you can see the Alert on UI
    time.sleep(2)
    # now you can accept or reject the dialog
    dialog.accept()
    # dialog.dismiss()

# so before you perform any action that will create the alert, you have to use the following line
TestBase.get_page().once("dialog", handle_alert_custom)

# the following would use the same mechanism to handle the alert throught the context of Browser or Page
# So unless you have a generic way of handling the alerts, use the 'once' method
TestBase.get_page().on("dialog", handle_alert_custom)

# if the above line is written / executed after the event, Playwright would be handling the alert on its own

# this line is generating the alert
box.click(button='right')

time.sleep(2)

TestBase.get_page().close()
