import socket
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep


# Utility Functions for common actions
def send_keys_to_element(driver, by, value, text, wait_time=20):
    """Send text to an element when clickable."""
    search_input = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable((by, value))
    )
    search_input.send_keys(text)


def wait_for_element_and_click(driver, by, value, wait_time=20):
    """Wait for an element to be clickable and click it, retry on StaleElementReferenceException."""
    retries = 5
    for _ in range(retries):
        try:
            element = WebDriverWait(driver, wait_time).until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
            return
        except StaleElementReferenceException:
            print("Element became stale. Retrying...")
            sleep(1)


def get_free_port():
    """Get a free port to use for Appium drivers."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))  # Bind to a free port provided by the OS
        return s.getsockname()[1]  # Get the port number


# Define the pickup and destination locations
pick_up = 'RUQB2805 جبل البويب قرطبة'
destination = 'Park Avenue'

# Bolt app options
options_bolt = UiAutomator2Options()
options_bolt.platform_name = "Android"
options_bolt.platform_version = "13"
options_bolt.device_name = "127.0.0.1:6569"
options_bolt.udid = "127.0.0.1:6569"  # The device ID of your emulator
options_bolt.app_package = "ee.mtakso.client"  # Package name of the Bolt app
options_bolt.app_activity = "ee.mtakso.client.activity.SplashHomeActivity"  # Main activity of the Bolt app
options_bolt.no_reset = True  # Keeps the app state between sessions
options_bolt.system_port = get_free_port()  # Dynamically assign a free port for Appium communication




# Connect to the Appium server
driver_bolt = webdriver.Remote(command_executor="http://localhost:4725", options=options_bolt)


try:
    # Terminate the app if running and then activate it
    driver_bolt.terminate_app("ee.mtakso.client")
    driver_bolt.activate_app("ee.mtakso.client")
    print("App activated successfully!")


    wait_for_element_and_click(driver_bolt, By.XPATH,
                                "//android.widget.FrameLayout[@resource-id='ee.mtakso.client:id/homeScreenContentContainer']/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.LinearLayout/android.view.ViewGroup"
)

    send_keys_to_element(driver_bolt, By.XPATH, "//android.widget.EditText[@hint='Destination']", destination)
    sleep(2)
    wait_for_element_and_click(driver_bolt, By.XPATH,
                                    "//androidx.recyclerview.widget.RecyclerView[@resource-id='ee.mtakso.client:id/addressesRecyclerView']/android.view.ViewGroup[1]")

    try:
        wait_for_element_and_click(driver_bolt, By.XPATH,
                                   "//android.widget.Button[@resource-id='ee.mtakso.client:id/confirm_button']")
        print("Confirm button clicked after selecting destination location.")
    except:
        print("No confirm button appeared after selecting destination location, continuing...")


    #Try to clear the text if the "Clear text" button is present
    try:
        clear_button = WebDriverWait(driver_bolt, 1).until(
            EC.element_to_be_clickable((By.XPATH, "//android.widget.ImageView[@content-desc='Clear text']"))
        )
        clear_button.click()
        print("Cleared the existing text in the search field.")
    except Exception as e:
        print("Clear text button not found, skipping clear action.")

    # Now send the pick-up location
    send_keys_to_element(driver_bolt, By.XPATH, "//android.widget.EditText[@text='Search pick-up location']", pick_up)

    # Wait for 2 seconds
    sleep(2)
    # Select the first suggestion for the pick-up location
    wait_for_element_and_click(driver_bolt, By.XPATH,
                               "//androidx.recyclerview.widget.RecyclerView[@resource-id='ee.mtakso.client:id/addressesRecyclerView']/android.view.ViewGroup[1]")

    #
    # try:
    #     wait_for_element_and_click(driver_bolt, By.XPATH,
    #                                "//android.widget.Button[@resource-id='ee.mtakso.client:id/confirm_button']")
    #     print("Confirm button clicked after selecting destination location.")
    # except:
    #     print("No confirm button appeared after selecting destination location, continuing...")


    try:
        price_element = WebDriverWait(driver_bolt, 60).until(
            EC.visibility_of_element_located(
                (By.XPATH,
                 '(//android.view.ViewGroup[@resource-id="ee.mtakso.client:id/rippleSupportContainer"])[1]//android.widget.TextView[@resource-id="ee.mtakso.client:id/primaryPrice"]')
            )
        )
        price_text = price_element.text
        print(f"Extracted price: {price_text}")
    except Exception as e:
        print("Failed to find the price element within the given time.")




    # Sleep to observe interaction
    sleep(500)  # Adjust the sleep time as necessary

finally:
    # Close the driver session
    driver_bolt.quit()
    print("Closed the Appium session.")