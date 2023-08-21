import time

from spearline_qa_src.lib.test_base import TestBase

url = "https://the-internet.herokuapp.com/horizontal_slider"

TestBase.get_page().goto(url)
time.sleep(2)
slider = TestBase.get_page().locator("xpath=//input")

width = slider.element_handle().bounding_box()["width"]
height = slider.element_handle().bounding_box()["height"]
slider_x = slider.element_handle().bounding_box()["x"]
slider_y = slider.element_handle().bounding_box()["y"]

print(f"width = {width} | height = {height}")
print(f"x = {slider_x} | y = {slider_y}")

# TestBase.get_page().mouse.move(slider_x, slider_y + int(width/2))
# time.sleep(1)
# TestBase.get_page().mouse.down()
# time.sleep(1)
# TestBase.get_page().mouse.move(slider_x + int(width/2), slider_y + int(width/2))
# time.sleep(1)
# TestBase.get_page().mouse.up()
# time.sleep(1)


# slider.drag_to(target=slider, source_position={"x": height/2, "y": 0}, target_position={"x": height/2, "y": width/2})

# -------------------------------------------------------
# #using the Locator's Click
# -------------------------------------------------------
# slider.click(position={"x": width/2, "y": height/2}, force=True)

# -------------------------------------------------------
# #using the mouse Click
# -------------------------------------------------------
# TestBase.get_page().mouse.click(x= slider_x+int(width/2), y=slider_y + int(height/2))

# -------------------------------------------------------
# #using the mouse move and click at that point (kind of Drag and Drop action)
# -------------------------------------------------------
TestBase.get_page().mouse.move(x= slider_x+int(width/2), y=slider_y + int(height/2))
TestBase.get_page().mouse.down()
time.sleep(2)
TestBase.get_page().mouse.move(x= slider_x+int(width/2) + 15, y=slider_y + int(height/2))
time.sleep(2)
TestBase.get_page().mouse.up()

time.sleep(2)
