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
    try:
        search_input = WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable((by, value))
        )
        search_input.clear()  # Clear any existing text
        search_input.send_keys(text)
    except Exception as e:
        print(f"Error sending keys to element ({by}, {value}): {e}")
        raise


# Function to wait for an element and click
def wait_for_element_and_click(driver, by, value, wait_time=20):
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable((by, value))
        )
        element.click()
    except Exception as e:
        print(f"Error clicking element ({by}, {value}): {e}")
        raise


# Define the pickup and destination locations
pick_up = 'qurtubah'
destination = 'Park Avenue'

# Careem app options (Targeting the emulator dynamically)
options_careem = UiAutomator2Options()
options_careem.platform_name = "Android"
options_careem.platform_version = "13"
options_careem.device_name = "127.0.0.1:6555"
options_careem.udid = "127.0.0.1:6555"
options_careem.app_package = "com.careem.acma"
options_careem.app_activity = "com.careem.superapp.feature.home.ui.SuperActivity"
options_careem.no_reset = True
options_careem.system_port = get_free_port()  # Dynamically assign a free port

# Uncomment and configure the following if you plan to interact with Uber as well
# from appium.options.android import UiAutomator2Options as UberOptions
# options_uber = UberOptions()
# options_uber.platform_name = "Android"
# options_uber.platform_version = "13"
# options_uber.device_name = "127.0.0.1:6563"  # Ensure different device name if using multiple emulators
# options_uber.udid = "127.0.0.1:6563"
# options_uber.app_package = "com.uber.android.app"
# options_uber.app_activity = "com.ubercab.rider.core.activities.SplashActivity"
# options_uber.no_reset = True
# options_uber.system_port = get_free_port()

try:
    # start_time = time()
    #
    driver = webdriver.Remote(
        command_executor='http://localhost:4725',
        options=options_careem
    )
    wait_for_element_and_click(driver, By.XPATH,"//android.view.ViewGroup[@resource-id='com.careem.acma:id/geo_fence_dialog_ok_button']/android.view.View")
    sleep(400)

    # # --- Launch Careem App ---
    # driver.terminate_app("com.careem.acma")  # Terminate if Careem is running
    # driver.activate_app("com.careem.acma")  # Launch Careem app
    #
    # sleep(2)  # Wait for the app to stabilize
    #
    # # Navigate to the search view for destination
    # wait_for_element_and_click(driver, By.XPATH, "(//android.view.View[@resource-id='Tile'])[1]/android.view.View")
    # wait_for_element_and_click(driver, By.XPATH,
    #                            "//android.widget.FrameLayout[@resource-id='com.careem.acma:id/search_view_container']")
    #
    # # Enter destination
    # send_keys_to_element(driver, By.ID, "com.careem.acma:id/search_view", destination)
    # sleep(1)  # Wait for suggestions to load
    #
    # # Select the first suggestion
    # wait_for_element_and_click(driver, By.XPATH,
    #                            "//androidx.recyclerview.widget.RecyclerView[@resource-id='com.careem.acma:id/search_recycler_view']/android.widget.LinearLayout[1]/android.widget.LinearLayout")
    #
    # # Navigate to the pickup location
    # wait_for_element_and_click(driver, By.XPATH,
    #                            "//android.widget.FrameLayout[@resource-id='com.careem.acma:id/map_pin_body_inner']")
    # wait_for_element_and_click(driver, By.XPATH,
    #                            "//android.widget.FrameLayout[@resource-id='com.careem.acma:id/parent_container']")
    #
    # # Enter pickup location
    # send_keys_to_element(driver, By.ID, "com.careem.acma:id/search_view", pick_up)
    # sleep(1)  # Wait for suggestions to load
    #
    # # Select the first suggestion for pickup
    # wait_for_element_and_click(driver, By.XPATH,
    #                            "//android.widget.FrameLayout[@resource-id='com.careem.acma:id/map_pin_body_inner']")
    #
    # # Confirm pickup location
    # wait_for_element_and_click(driver, By.XPATH, "//android.view.ViewGroup[@content-desc='Confirm pickup']")
    #
    # # Extract Careem price
    # try:
    #     price_element_careem = WebDriverWait(driver, 30).until(
    #         EC.visibility_of_element_located((By.XPATH,
    #                                           '(//android.widget.LinearLayout[@resource-id="com.careem.acma:id/productCardContent"])[1]/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.LinearLayout'))
    #     )
    #     price_text_element_careem = price_element_careem.find_element(By.XPATH, './/android.widget.TextView')
    #     price_text = price_text_element_careem.text
    #     print(f"Careem Price: {price_text}")
    # except Exception as e:
    #     print(f"Error extracting Careem price: {e}")
    #
    # end_time = time()
    # total_time = end_time - start_time
    # print(f"Total time taken: {total_time:.2f} seconds")
    #
    # # Optional: Add any additional logic here, such as interacting with Uber if configured

except Exception as e:
    print(f"An error occurred: {e}")

