"""
rpa.py
This module encapsulates the Selenium library into utility functions to make code less verbose
and more Pythonic. It uses XPath as the default locator for interacting with page elements.
Key Features:
- Simplifies common operations such as clicking, filling input fields, retrieving text, and checking element presence.
- Reduces boilerplate code by encapsulating explicit wait configurations.
- Some functions offer a `timeout` parameter to customize wait times, providing flexibility for varying application response times.
- Provides a cleaner and more intuitive interface for element manipulation.
- Supports custom exception handling and logging.
Usage Example:
    import rpa
    # Navigate to a URL
    rpa.get("http://www.myurl.com")
    # Click a button
    rpa.click("//button[@id='submit']")
    # Fill a text field
    rpa.send("//input[@name='username']", "my_user")
    # Get the text of an element
    text = rpa.find("//div[@class='message']").text
Requirements:
- Selenium WebDriver must be configured and available.
- Familiarity with XPath for locating elements is recommended.
Conventions:
- XPath is the default locator for elements.
Author:
Edilson Wagner Ribeiro - EdPyDev
edpydev@gmail.com
ewribeiro (GitHub)
"""

import time
from functools import cache
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from typing import List
import os
from loguru import logger


@cache
def get_driver() -> Chrome:
    """
    Initializes a new Chrome WebDriver instance with custom configurations and maximizes the window.
    This function uses the @cache decorator from functools to ensure that the same WebDriver instance is reused for subsequent calls,
    avoiding redundant initializations and improving performance.
    The use of caching is particularly beneficial when creating a new WebDriver instance is resource-intensive.
    Features:
        - Configures a custom user agent for the browser.
        - Runs in headless mode for better performance in non-interactive environments.
        - Disables notifications and certain automation flags to minimize interference.
        - Sets the download directory to 'Downloads' in the user's home folder. The directory is created
          if it does not already exist.
        - Ensures downloaded PDF files are saved directly without showing a prompt, and prevents
          PDFs from being opened in the browser.
    Returns:
        Chrome: A cached instance of the Chrome WebDriver.
    """

    # Configure download directory
    user_home = os.path.expanduser("~")
    download_dir = os.path.join(user_home, "Downloads")
    os.makedirs(download_dir, exist_ok=True)

    options = Options()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")
    # options.add_argument("--headless=new")
    options.add_argument("--disable-notifications")
    options.add_experimental_option(
        "excludeSwitches", ["enable-logging", "enable-automation"]
    )
    options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,
            "plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
        },
    )
    driver = Chrome(options=options)
    driver.set_window_size(1920, 1080)
    driver.maximize_window()
    return driver


def get(url: str):
    """
    Navigates the web driver to a specific URL and maximizes the window.
    Args:
        url (str): The URL to navigate to.
    """
    get_driver().get(url=url)


@cache
def get_action() -> ActionChains:
    """
    Creates an ActionChains object for performing complex user interactions.
    Returns:
        ActionChains: An ActionChains object for user interactions.
    """
    return ActionChains(get_driver())


@cache
def get_wait(timeout: int = 12) -> WebDriverWait:
    """
    Creates a WebDriverWait object with a specific timeout.
    Args:
        timeout (int, optional): The maximum wait time in seconds. Defaults to 30.
    Returns:
        WebDriverWait: A WebDriverWait object for explicit waits.
    """
    driver = get_driver()
    wait = WebDriverWait(driver, timeout, 1)
    return wait


def wait_alert(timeout: int = 12) -> None:
    """
    Waits for an alert to be present.
    Args:
        timeout (int): Maximum wait time in seconds. Defaults to 3.
    """
    get_wait(timeout).until(EC.alert_is_present())


def wait_clickable(xpath: str, timeout: int = 12) -> WebElement:
    """
    Waits for the specified element to be clickable.
    Args:
        xpath (str): XPath of the element.
        timeout (int): Maximum wait time in seconds. Defaults to 3.
    """
    return get_wait(timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))


def wait_frame(xpath: str, timeout: int = 12) -> None:
    """
    Waits for the specified frame to be available and switches to it.
    Args:
        xpath (str): XPath of the frame.
        timeout (int): Maximum wait time in seconds. Defaults to 3.
    """
    get_wait(timeout).until(
        EC.frame_to_be_available_and_switch_to_it((By.XPATH, xpath))
    )


def wait_invisibility(xpath: str, timeout: int = 12) -> None:
    """
    Waits for the specified element to be invisible.
    Args:
        xpath (str): XPath of the element.
        timeout (int): Maximum wait time in seconds. Defaults to 3.
    """
    get_wait(timeout).until(EC.invisibility_of_element_located((By.XPATH, xpath)))


def wait_selectable(xpath: str, timeout: int = 12) -> WebElement:
    """
    Waits for the specified element to be selected.
    Args:
        xpath (str): XPath of the element.
        timeout (int): Maximum wait time in seconds. Defaults to 3.
    """
    return get_wait(timeout).until(EC.element_to_be_selected((By.XPATH, xpath)))


def wait_text_attribute(
    xpath: str, attribute: str, text: str, timeout: int = 12
) -> None:
    """
    Waits for a specific text to be present in an element's attribute.
    Args:
        xpath (str): XPath of the element.
        attribute (str): Name of the attribute.
        text (str): Expected text in the attribute.
        timeout (int): Maximum wait time in seconds. Defaults to 3.
    """
    get_wait(timeout).until(
        EC.text_to_be_present_in_element_attribute((By.XPATH, xpath), attribute, text)
    )


def wait_partial_url(url: str, timeout: int = 12) -> None:
    """
    Espera que a URL atual contenha a string especificada.
    Args:
        url (str): Substring da URL esperada.
        timeout (int): Tempo máximo de espera em segundos. Defaults to 3.
    """
    get_wait(timeout).until(EC.url_contains(url))


def wait_visibility(xpath: str, timeout: int = 12) -> None:
    """
    Waits for the current URL to contain the specified string.
    Args:
        url (str): Substring of the expected URL.
        timeout (int): Maximum wait time in seconds. Defaults to 3.
    """
    return get_wait(timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))


def wait_all_visible(xpath: str, timeout: int = 12) -> List[WebElement]:
    """
    Waits for all specified elements to be visible.
    Args:
        xpath (str): XPath of the elements.
        timeout (int): Maximum wait time in seconds. Defaults to 3.
    """
    return get_wait(timeout).until(
        EC.visibility_of_all_elements_located((By.XPATH, xpath))
    )


def wait_new_window(timeout: int = 12) -> None:
    """
    Waits for a new window to be opened.
    Args:
        timeout (int): Maximum wait time in seconds. Defaults to 3.
    """
    get_wait(timeout).until(EC.new_window_is_opened(get_driver().window_handles))


def find(xpath: str, timeout: int = 12) -> WebElement:
    """
    Finds a web element based on its XPath.
    Args:
        xpath (str): The XPath of the element to find.
    Returns:
        WebElement: The found web element.
    """
    return wait_visibility(xpath, timeout)


def find_all(xpath: str, timeout: int = 12) -> List[WebElement]:
    """
    Finds all web elements matching a specific XPath.
    Args:
        xpath (str): The XPath to find elements.
    Returns:
        List[WebElement]: A list of all found web elements.
    """
    return wait_all_visible(xpath, timeout)


def click(xpath: str, timeout: int = 12):
    """
    Clicks on a web element located by its XPath.
    Args:
        xpath (str): The XPath of the element to click.
    """
    wait_clickable(xpath, timeout).click()


def send(xpath: str, text: str, timeout: int = 12):
    """
    Sends text to a web element located by its XPath.
    Args:
        xpath (str): The XPath of the element to send text to.
        text (str): The text to send.
    """
    wait_clickable(xpath, timeout).send_keys(text)


def select_by_value(xpath: str, value: str, timeout: int = 12):
    """
    Selects an option from a dropdown element using its value.
    Args:
        xpath (str): The XPath of the dropdown element.
        value (str): The value of the option to select.
    """
    Select(wait_clickable(xpath, timeout)).select_by_value(value)


def select_by_visible_text(xpath: str, visible_text: str, timeout: int = 12) -> None:
    """
    Selects an option from a dropdown element using its visible text.
    Args:
        xpath (str): The XPath of the dropdown element.
        visible_text (str): The visible text of the option to select.
    """
    Select(wait_clickable(xpath, timeout)).select_by_visible_text(visible_text)


def is_selected(xpath: str, timeout: int = 12) -> bool:
    """
    Checks if an element is selected.
    Args:
        xpath (str): The XPath of the element to check.
    Returns:
        bool: True if the element is selected, False otherwise.
    """
    return get_wait(timeout).until(
        EC.element_selection_state_to_be(find(xpath, timeout), True)
    )


def is_not_selected(xpath: str, timeout: int = 12) -> bool:
    """
    Checks if an element is not selected.
    Args:
        xpath (str): The XPath of the element to check.
    Returns:
        bool: True if the element is not selected, False otherwise.
    """
    return get_wait(timeout).until(EC.element_selection_state_to_be(find(xpath), False))


def is_displayed(xpath: str, timeout: int = 12) -> bool:
    """
    Checks if the last element found by the XPath is visible.
    Args:
        xpath (str): The XPath to find the elements.
    Returns:
        bool: True if the last element is visible, False otherwise.
    """
    return find_all(xpath, timeout) and find_all(xpath, timeout)[-1].is_displayed()


def select_js(option_value: str) -> None:
    """
    Selects an option in a select element using JavaScript.
    Args:
        option_value (str): The value of the option to be selected.
    """
    script = (
        f'''document.querySelector('[value="{option_value}"]').selected="selected"'''
    )
    get_driver().execute_script(script)


def set_value_js(css_selector: str, value: str) -> None:
    """
    Sets the value of an element using JavaScript.
    Args:
        css_selector (str): The CSS selector of the element.
        value (str): The new value of the element.
    """
    script = f'''document.querySelector('{css_selector}').value="{value}"'''
    get_driver().execute_script(script)


def click_js(css_selector: str) -> None:
    """
    Clicks on an element using JavaScript.
    Args:
        css_selector (str): The CSS selector of the element.
    """
    script = f"""document.querySelector('{css_selector}').click()"""
    get_driver().execute_script(script)


def quit() -> None:
    """
    Closes the browser and ends the WebDriver session.
    """
    get_driver().quit()


def sleep(seconds: int) -> None:
    """
    Pauses the execution of the script for a given number of seconds.
    Args:
        seconds (int): The number of seconds to pause.
    """
    time.sleep(seconds)


def run_script(script: str) -> None:
    """
    Executes a JavaScript script in the context of the browser.
    Args:
        script (str): The JavaScript script to be executed.
    """
    get_driver().execute_script(script)


def scroll_start() -> None:
    """
    Scrolls the page to the top.
    """
    get_driver().execute_script("window.scrollTo(0, 0);")


def scroll_end() -> None:
    """
    Scrolls the page to the bottom.
    """
    get_driver().execute_script("window.scrollTo(0, document.body.scrollHeight);")


def keys() -> Keys:
    """
    Returns a Keys object to simulate keyboard actions.
    Returns:
        Keys: The Keys object from Selenium.
    """
    return Keys


def exit_iframe() -> None:
    """
    Exits the current iframe and returns to the main page context.
    """
    get_driver().switch_to.default_content()


def switch_window(n: int) -> None:
    """
    Switches to the specified window.
    Args:
        n (int): The window number.
    """
    get_driver().switch_to.window(get_driver().window_handles[n])


def close() -> None:
    """
    Closes the current window.
    """
    get_driver().close()


def screenshot(filename: str) -> None:
    """
    Saves a screenshot of the current window to a PNG image file.
    """
    get_driver().save_screenshot(filename)


def wait_download(file_path: str, check_interval: int = 1, max_equal_readings: int = 3):
    """
    Ensures that a file download is complete by monitoring the file size
    at regular intervals and stopping when the size remains the same for
    a defined number of consecutive readings.
    :param file_path: Path to the file to be monitored.
    :param check_interval: Time interval (in seconds) between readings.
    :param max_equal_readings: Number of consecutive readings with the same size to stop the monitoring.
    """
    while not os.path.isfile(file_path):
        logger.error(f"Arquivo não encontrado: {file_path}")
        time.sleep(1)
    previous_size = -1
    equal_readings = 0
    while equal_readings < max_equal_readings:
        current_size = os.path.getsize(file_path)
        if current_size == previous_size:
            equal_readings += 1
        else:
            equal_readings = 0
        previous_size = current_size
        logger.info(
            f"Tamanho do arquivo: {current_size} bytes. Leituras iguais consecutivas: {equal_readings}"
        )
        if equal_readings < max_equal_readings:
            time.sleep(check_interval)
    logger.info(
        f"Tamanho final do arquivo: {current_size} bytes. Monitoramento encerrado."
    )
    return current_size