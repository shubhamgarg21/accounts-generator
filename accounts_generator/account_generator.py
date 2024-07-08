from .proxy_generator import ProxyGenerator
from .user_agent_handler import UserAgentHandler
from .chrome_driver import ChromeDriver

from PIL import Image
from selenium.webdriver.remote.webelement import WebElement

import time, os, json, random


class AccountGenerator:
    def __init__(self, wait_time=2, use_proxy=True, use_user_agent=True):
        self.proxy_generator = None
        self.user_agent_handler = None
        if use_proxy:
            self.proxy_generator = ProxyGenerator()
        if use_user_agent:
            self.user_agent_handler = UserAgentHandler()
        self.driver = None
        self.wait_time = wait_time
        self.sleep_time = 2

    def take_screenshot(self, element):
        # Locate the element
        # element = self.driver.find_element_by_id(uri)

        # Take a screenshot of the entire page
        self.driver.save_screenshot("page_screenshot.png")

        # Get the element's location and size
        location = element.location
        size = element.size

        # Open the screenshot and crop it to the element's bounds
        x = location['x']
        y = location['y']
        width = location['x'] + size['width']
        height = location['y'] + size['height']
        image = Image.open("page_screenshot.png")
        element_image = image.crop((x, y, width, height))

        # Save the cropped image
        element_image.save("element_screenshot.png")

    def start_driver(self):
        if self.driver:
            self.close_driver()
        proxy = self.proxy_generator.get_valid_proxy() if self.proxy_generator else None
        user_agent = self.user_agent_handler.get_user_agent() if self.user_agent_handler else None
        self.driver = ChromeDriver(proxy=proxy, user_agent=user_agent).prepare_driver()
    
    def close_driver(self):
        if self.driver:
            self.driver.quit()

    def enter_text(self, element: WebElement, text: str):
        for character in text:
            element.send_keys(character)
            time.sleep(random.uniform(.07, .15))

    def save_account_details(self, account_details, file='generated.json'):
        # Convert the dictionary to JSON format
        account_json = json.dumps(account_details)
        # Write the JSON data to a file
        with open(file, 'a') as f:
            # Check if the file is empty
            if os.path.exists(file) and os.path.getsize(file) > 0:
                f.write("\n")
            f.write(account_json)
            print("Account details saved to {}".format(file))   

    # create destructor
    def __del__(self):
        self.close_driver()
        print('Chrome driver closed.')
