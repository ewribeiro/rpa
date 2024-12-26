import time
from functools import cache
from typing import Literal
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from typing import List


@cache
def get_driver() -> Chrome:
    """
    Initializes a new Chrome WebDriver instance and maximizes the window.

    Returns:
        Chrome: A new Chrome WebDriver instance.
    """
    driver = Chrome()
    driver.maximize_window()
    return driver


def get_wait(timeout: int = 30) -> WebDriverWait:
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


def get_action() -> ActionChains:
    """
    Creates an ActionChains object for performing complex user interactions.

    Returns:
        ActionChains: An ActionChains object for user interactions.
    """
    driver = get_driver()
    action = ActionChains(driver)
    return action


def get(url: str):
    """
    Navigates the web driver to a specific URL and maximizes the window.

    Args:
        url (str): The URL to navigate to.
    """
    driver = get_driver()
    driver.maximize_window()
    driver.get(url=url)


def find(xpath: str) -> WebElement:
    """
    Finds a web element based on its XPath.

    Args:
        xpath (str): The XPath of the element to find.

    Returns:
        WebElement: The found web element.
    """
    driver = get_driver()
    element = driver.find_element(By.XPATH, xpath)
    wait = get_wait()
    wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    return element


def find_all(xpath: str) -> List[WebElement]:
    """
    Finds all web elements matching a specific XPath.

    Args:
        xpath (str): The XPath to find elements.

    Returns:
        List[WebElement]: A list of all found web elements.
    """
    driver = get_driver()
    elements = driver.find_elements(By.XPATH, xpath)
    return elements


def click(xpath: str):
    """
    Clicks on a web element located by its XPath.

    Args:
        xpath (str): The XPath of the element to click.
    """
    driver = get_driver()
    wait = get_wait()
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    driver.find_element(By.XPATH, xpath).click()


def send(xpath: str, text: str):
    """
    Sends text to a web element located by its XPath.

    Args:
        xpath (str): The XPath of the element to send text to.
        text (str): The text to send.
    """
    driver = get_driver()
    wait = get_wait()
    wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    driver.find_element(By.XPATH, xpath).send_keys(text)


def select_by_value(xpath: str, value: str):
    """
    Selects an option from a dropdown element using its value.

    Args:
        xpath (str): The XPath of the dropdown element.
        value (str): The value of the option to select.
    """
    driver = get_driver()
    element = driver.find_element(By.XPATH, xpath)
    Select(element).select_by_value(value)


def select_by_visible_text(xpath: str, visible_text: str) -> None:
    """
    Selects an option from a dropdown element using its visible text.

    Args:
        xpath (str): The XPath of the dropdown element.
        visible_text (str): The visible text of the option to select.
    """
    element: WebElement = find(xpath)  # Obtém o elemento usando a função 'find'
    Select(element).select_by_visible_text(visible_text)


def is_selected(xpath: str) -> bool:
    """
    Verifica se um elemento está selecionado.

    Args:
        xpath (str): The XPath of the element to check.

    Returns:
        bool: True se o elemento estiver selecionado, False caso contrário.
    """
    element: WebElement = find(xpath)  # Obtém o elemento usando a função 'find'
    wait = get_wait()
    return wait.until(EC.element_selection_state_to_be(element, True))


def is_not_selected(xpath: str) -> bool:
    """
    Verifica se um elemento não está selecionado.

    Args:
        xpath (str): The XPath of the element to check.

    Returns:
        bool: True se o elemento não estiver selecionado, False caso contrário.
    """
    element: WebElement = find(xpath)  # Obtém o elemento usando a função 'find'
    wait = get_wait()
    return wait.until(EC.element_selection_state_to_be(element, False))


def is_displayed(xpath: str) -> bool:
    """
    Verifica se o último elemento encontrado pelo XPath está visível.

    Args:
        xpath (str): The XPath to find the elements.

    Returns:
        bool: True se o último elemento estiver visível, False caso contrário.
    """
    elements: List[WebElement] = find_all(xpath)  # Obtém os elementos usando a função 'find_all'
    return elements and elements[-1].is_displayed()


def wait(
    type: Literal["alert", "click", "frame", "invisibility", "select", "text_attribute", "url", "visibility", "visibility_all", "window"],
    xpath: str = None,
    url: str = None,
    atribute: str = None,
    text: str = None,
    timeout = 3
) -> None:
    """
    Espera uma condição explícita no Selenium WebDriver com base no tipo de espera especificado.

    Args:
        type (Literal): O tipo de espera a ser realizada.
        xpath (str, optional): O xpath do elemento (se aplicável).
        url (str, optional): URL parcial a ser verificada (se aplicável).
        atribute (str, optional): O atributo do elemento a ser verificado (se aplicável).
        text (str, optional): O texto a ser verificado no atributo do elemento (se aplicável).
        timeout (int, optional): Tempo máximo de espera em segundos. Defaults to 3.
    """
    driver = get_driver()
    wait = get_wait(timeout=timeout)

    match type:
        case "alert":
            wait.until(EC.alert_is_present((By.XPATH, xpath)))
        case "click":
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        case "frame":
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, xpath)))
        case "invisibility":
            wait.until(EC.invisibility_of_element_located((By.XPATH, xpath)))
        case "select":
            wait.until(EC.element_to_be_selected((By.XPATH, xpath)))
        case "text_attribute":
            wait.until(
                EC.text_to_be_present_in_element_attribute((By.XPATH, xpath), atribute, text)
            )
        case "url":
            wait.until(EC.url_contains(url))
        case "visibility":
            wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        case "visibility_all":
            wait.until(EC.visibility_of_all_elements_located((By.XPATH, xpath)))
        case "window":
            wait.until(EC.new_window_is_opened(driver.window_handles))


def select_js(option_value: str) -> None:
    """
    Seleciona uma opção em um elemento select usando JavaScript.

    Args:
        option_value (str): O valor da opção a ser selecionada.
    """
    driver = get_driver()
    script = f'''document.querySelector('[value="{option_value}"]').selected="selected"'''
    driver.execute_script(script)


def set_value_js(css_selector: str, value: str) -> None:
    """
    Define o valor de um elemento usando JavaScript.

    Args:
        css_selector (str): O seletor CSS do elemento.
        value (str): O novo valor do elemento.
    """
    driver = get_driver()
    script = f'''document.querySelector('{css_selector}').value="{value}"'''
    driver.execute_script(script)


def click_js(css_selector: str) -> None:
    """
    Clica em um elemento usando JavaScript.

    Args:
        css_selector (str): O seletor CSS do elemento.
    """
    driver = get_driver()
    script = f"""document.querySelector('{css_selector}').click()"""
    driver.execute_script(script)


def quit() -> None:
    """
    Fecha o navegador e encerra a sessão do WebDriver.
    """
    driver = get_driver()
    driver.quit()


def sleep(n: int) -> None:
    """
    Pausa a execução do script por um determinado número de segundos.

    Args:
        n (int): O número de segundos para pausar.
    """
    time.sleep(n)


def run_script(script: str) -> None:
    """
    Executa um script JavaScript no contexto do navegador.

    Args:
        script (str): O script JavaScript a ser executado.
    """
    driver = get_driver()
    driver.execute_script(script)


def scroll_start() -> None:
    """
    Rola a página para o topo.
    """
    driver = get_driver()
    driver.execute_script("window.scrollTo(0, 0);")


def scroll_end() -> None:
    """
    Rola a página para o final.
    """
    driver = get_driver()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def keys() -> Keys:
    """
    Retorna um objeto Keys para simular ações de teclado.

    Returns:
        Keys: O objeto Keys do Selenium.
    """
    return Keys


def exit_iframe() -> None:
    """
    Sai do iframe atual e retorna para o contexto principal da página.
    """
    driver = get_driver()
    driver.switch_to.default_content()