import socket
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep, time

# Function to find an available port dynamically
def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))  # Bind to a free port provided by the OS
        return s.getsockname()[1]  # Get the port number

# Tap at specific coordinates
def tap_at_coordinates(driver, x, y, pause_time=0.2):
    touch_input = PointerInput(interaction.POINTER_TOUCH, "touch")
    actions = ActionBuilder(driver, mouse=touch_input)
    actions.pointer_action.move_to_location(x, y)
    actions.pointer_action.pointer_down()  # Simulate touch down
    actions.pointer_action.pause(pause_time)  # Pause for a short duration (default 200 milliseconds)
    actions.pointer_action.pointer_up()  # Simulate touch up
    actions.perform()

# Function to send text to an element
def send_keys_to_element(driver, by, value, text, wait_time=20):
    search_input = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable((by, value))
    )
    search_input.send_keys(text)

# Function to wait for an element and click
def wait_for_element_and_click(driver, by, value, wait_time=20):
    element = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable((by, value))
    )
    element.click()

# Define the pickup and destination locations
pick_up = 'RUQB2805 جبل البويب قرطبة'
destination = 'Park Avenue'

# Careem app options (Targeting the emulator dynamically)
options_jeeny = UiAutomator2Options()
options_jeeny.platform_name = "Android"
options_jeeny.platform_version = "13"
options_jeeny.device_name = "127.0.0.1:6555"
options_jeeny.udid = "127.0.0.1:6555"
options_jeeny.app_package = "me.com.easytaxi"
options_jeeny.app_activity = "me.com.easytaxi.v2.ui.ride.activities.RideRequestFlowActivity"
options_jeeny.no_reset = True
options_jeeny.system_port = get_free_port()



start_time = time()

driver_jeeny = webdriver.Remote(
        command_executor='http://localhost:4725',  # No /wd/hub in Appium 2.x
        options=options_jeeny
)

sleep(400)

#     # --- Launch Apps ---
#     driver_jeeny.terminate_app("me.com.easytaxi")
#     driver_jeeny.activate_app("me.com.easytaxi")
#
#     wait_for_element_and_click(driver_jeeny, By.XPATH,"//android.view.ViewGroup[@resource-id='me.com.easytaxi:id/clWhereToCard']")
#
#     send_keys_to_element(driver_jeeny, By.ID, "me.com.easytaxi:id/dropOffAddress", destination)
#
#     wait_for_element_and_click(driver_jeeny, By.XPATH,"//androidx.recyclerview.widget.RecyclerView[@resource-id='me.com.easytaxi:id/rvAddresses']/android.widget.RelativeLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout")
#     wait_for_element_and_click(driver_jeeny, By.XPATH,"//android.widget.ImageView[@resource-id='me.com.easytaxi:id/searchLens']")
#
#     send_keys_to_element(driver_jeeny, By.ID, "me.com.easytaxi:id/pickUpAddress", pick_up)
#     sleep(2)
#     wait_for_element_and_click(driver_jeeny, By.XPATH,"//androidx.recyclerview.widget.RecyclerView[@resource-id='me.com.easytaxi:id/rvAddresses']/android.widget.RelativeLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout")
#
#
#     wait_for_element_and_click(driver_jeeny, By.XPATH,"//android.widget.Button[@resource-id='me.com.easytaxi:id/btnDone']")
#
#
#     try:
#         # Wait for the price element to be visible using its resource-id
#         price_element = WebDriverWait(driver_jeeny, 20).until(
#             EC.visibility_of_element_located(
#                 (By.XPATH, "//android.widget.TextView[@resource-id='me.com.easytaxi:id/text_estimated_price']"))
#         )
#     except:
#         print("Price element not found")
#     price = price_element.text
#     print(f"Jeeny Price: {price}")
#
#
#     sleep(600)  # Wait for apps to open
#
# except Exception as e:
#     print(f"An error occurred: {e}")