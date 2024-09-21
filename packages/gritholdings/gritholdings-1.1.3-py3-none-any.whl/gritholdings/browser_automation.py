import time
from typing import List, Any, Optional
from selenium.webdriver.common.by import By


class BrowserAutomation:
    def find_deep_shadow_element(driver, start_element=None):
        if start_element is None:
            current_element = driver.execute_script("return document.documentElement")
        else:
            current_element = start_element
        
        while True:
            shadow_root = driver.execute_script('return arguments[0].shadowRoot', current_element)
            if not shadow_root:
                break
            current_element = shadow_root
        return current_element

    def find_elements_contain_in_shadow_dom(driver, selector: str, text: str) -> List[Any]:
        """
        Searches for elements that contain a given text inside the deepest shadow DOM from the document root or a given starting element.
        
        Parameters:
        - driver: The Selenium WebDriver instance.
        - selector: The CSS selector to find elements.
        - text: The text to search within the elements.
        
        Returns:
        - A list of elements that match the criteria.
        """
        
        # Navigate to the deepest shadow DOM or element context
        context_element = find_deep_shadow_element(driver)
        
        result_elements = []
        if selector is not None and selector != '':
            target_elements = context_element.find_elements(By.CSS_SELECTOR, selector)
            for elem in target_elements:
                if text in elem.text:
                    result_elements.append(elem)
        else:
            # If no selector is defined, search all elements with any tags
            result_elements = context_element.find_elements(By.XPATH, f"//*[text()[contains(.,'{text}')]]")
        
        return result_elements

    def find_elements_contain(driver, selector:str, text:str):
        result_elements = []
        if selector is not None and selector != '':
            target_elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for element in target_elements:
                if text in element.text:
                    result_elements.append(element)
        else:
            # if no selector is defined, search all elements with any tags
            # useful when the text inside is unique enough
            # source: https://stackoverflow.com/questions/3655549/xpath-containstext-some-string-
            # doesnt-work-when-used-with-node-with-more
            result_elements = driver.find_elements(By.XPATH, f"//*[text()[contains(.,'{text}')]]")
        return result_elements

    def wait_till(element, texts: Optional[List[str]] = None, css_selector: Optional[str] = None,
            timeout: int = 5):
        """
        Newer version compared to wait_until
        Wait until elements with at least one from the contained texts or with the given CSS selector appear.
        """
        if not texts and not css_selector:
            raise ValueError('Either texts or css_selector must be provided.')

        is_element_found = False
        tries = 0
        delay = 0.5
        max_tries = timeout / delay
        while not is_element_found and tries < max_tries:
            # do not use WebDriverWait since it is not working properly
            time.sleep(delay)
            if css_selector:
                try:
                    element.find_element(By.CSS_SELECTOR, css_selector)
                    is_element_found = True
                except:
                    pass
            else:
                for text in texts:
                    if is_element_found is True:
                        break
                    try:
                        element.find_element(By.XPATH, f"//*[contains(text(), '{text}')]")
                        is_element_found = True
                    except:
                        pass
            tries += 1