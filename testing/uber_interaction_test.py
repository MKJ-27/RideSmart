import socket
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


def wait_for_element_and_click(driver, by, value, wait_time=60):
    """Wait for an element to be clickable and click it with a longer wait time."""
    element = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable((by, value))
    )
    print(f"Clicking on element: {value}")
    element.click()


def send_keys_to_element(driver, by, value, text, wait_time=30):
    """Wait for an element to be clickable and send keys to it."""
    element = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable((by, value))
    )
    print(f"Sending text '{text}' to element: {value}")
    element.send_keys(text)

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))  # Bind to a free port provided by the OS
        return s.getsockname()[1]  # Get the port number

# Define the pickup and destination locations
pick_up = 'RUQB2805 جبل البويب قرطبة'
destination = 'Park Avenue'

# Set up options for Uber app automation
options_uber = UiAutomator2Options()
options_uber.platform_name = "Android"
options_uber.platform_version = "13"
options_uber.device_name = "127.0.0.1:655"  # Emulator or device's IP:Port
options_uber.udid = "127.0.0.1:6555"  # Unique device identifier
options_uber.app_package = "com.ubercab"
options_uber.app_activity = "com.ubercab/.presidio.app.core.root.RootActivity"
options_uber.no_reset = True  # Avoid resetting the app state between sessions
options_uber.system_port = get_free_port()  # Set system port to avoid conflicts

# Initialize WebDriver for Uber app
driver_uber = webdriver.Remote(
    command_executor='http://localhost:4725',  # No /wd/hub in Appium 2.x
    options=options_uber
)

sleep(400)

# try:
#     # Terminate and relaunch the Uber app
#     driver_uber.terminate_app("com.ubercab")
#     driver_uber.activate_app("com.ubercab")
#     sleep(6)  # Wait for the app to load
#
#     # --- Step 1: Click on the 'Enter destination' field ---
#     wait_for_element_and_click(driver_uber, By.XPATH, "//android.widget.TextView[@content-desc='Enter destination']")
#     sleep(2)
#
#     wait_for_element_and_click(driver_uber, By.XPATH, "//android.widget.TextView[@resource-id='com.ubercab:id/ub__location_edit_search_pickup_view']")
#
#     # --- Step 3: Send the pickup location ---
#     send_keys_to_element(driver_uber, By.XPATH, "//android.widget.EditText[@resource-id='com.ubercab:id/ub__location_edit_search_pickup_edit']", pick_up)
#     sleep(2)
#     wait_for_element_and_click(driver_uber, By.XPATH, "//android.widget.LinearLayout[@resource-id='com.ubercab:id/ub__text_search_v2_results']/android.widget.FrameLayout[1]")
#
#
#     send_keys_to_element(driver_uber, By.XPATH, "//android.widget.EditText[@resource-id='com.ubercab:id/ub__location_edit_search_destination_edit']", destination)
#     sleep(2)
#     wait_for_element_and_click(driver_uber, By.XPATH, "//android.widget.LinearLayout[@resource-id='com.ubercab:id/ub__text_search_v2_results']/android.widget.FrameLayout[1]")
#
#     try:
#         # Locate the UberX product container (or similar identifiers related to UberX)
#         uberx_element = WebDriverWait(driver_uber, 20).until(
#             EC.visibility_of_element_located((By.XPATH,
#                                               '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.ubercab:id/flex_product_selection_recycler_view_id"]//android.view.ViewGroup[.//android.widget.TextView[contains(@text, "UberX")]]'
#                                               ))
#         )
#
#         # Now find the price associated with UberX by navigating to its price container
#         price_element = uberx_element.find_element(By.XPATH,
#                                                    './/android.view.ViewGroup[@resource-id="com.ubercab:id/ub__flex_cell_primaryTrailing"]//android.widget.TextView'
#                                                    )
#
#         # Extract the price text
#         price_text = price_element.text
#
#         print(f"UberX Price: {price_text}")
#
#     except Exception as e:
#         print(f"Error extracting UberX price: {e}")
#
#
#     sleep(600)
#
# except Exception as e:
#     print(f"An error occurred: {e}")
#
# finally:
#     # Close the session
#     driver_uber.quit()