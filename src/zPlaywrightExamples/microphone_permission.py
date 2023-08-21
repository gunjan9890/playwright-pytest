import time

from playwright.sync_api import sync_playwright, Browser, Page

permissions = ['--use-fake-ui-for-media-stream']
# more such permission find here
# https://webrtc.github.io/webrtc-org/testing/

browser: Browser = sync_playwright().start().chromium.launch(headless=False, channel='chrome', slow_mo=100, args=permissions)
page: Page = browser.new_page()

page.goto('https://platform.spearline.com/admin/user/login')
if page.title() == "Login":
    page.locator("xpath=//input[@name='email'] >> visible=true").fill('qa.service@spearline.com')
    page.locator("xpath=//input[@name='password'] >> visible=true").fill('T3STp4ss!')
    page.locator("xpath=//input[@id='log-in']").click()

page.wait_for_load_state(timeout=60000)

# this page requires the microphone permission
# if you remove the permission from the top array, you will find a pop-up asking for permission
# but using the given permission, you wont need
page.goto("https://platform.spearline.com/admin/voice-assure-realtime")

time.sleep(5)
page.close()
