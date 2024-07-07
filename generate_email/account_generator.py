from .proxy_generator import ProxyGenerator
from .user_agent_handler import UserAgentHandler
from .chrome_driver import ChromeDriver
from .check_availability import check_email_availability
from .fake_account_data import generate_fake_data

from PIL import Image
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import time, os, json, random, uuid


SIGNUP_URL = 'https://signup.live.com/signup'
ID_USERNAME = 'usernameInput'
ID_PASSWORD = 'Password'
ID_FIRST_NAME = 'firstNameInput'
ID_LAST_NAME = 'lastNameInput'
ID_BIRTH_MONTH = 'BirthMonth'
ID_BIRTH_DAY = 'BirthDay'
ID_BIRTH_YEAR = 'BirthYear'
ID_NEXT_BUTTON = 'nextButton'
ID_ACCEPT_BUTTON = 'acceptButton'


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

    def open_signup_page(self):
            time.sleep(self.sleep_time)
            self.driver.get(SIGNUP_URL)

    def create_account(self, data=None):
        if data == None:
            data = generate_fake_data()
            while not check_email_availability(data['email']):
                print(f"Email {data['email']} is not available.")
                data = generate_fake_data()
        else :
            if not check_email_availability(data['email']):
                print(f"Email {data['email']} is not available.")

                # check if alternate_email key is present in data
                if 'alternate_emails' in data.keys():
                    available_email = None
                    for email in data['alternate_emails']:
                        if check_email_availability(email):
                            available_email = email
                            break
                    
                    if available_email:
                        data['email'] = available_email
                        print(f"Alternate email {available_email} is available.")
                    else:
                        print("No alternate email available.")
                        print("Account generation failed.")
                        return
                else:
                    print("No alternate email provided.")
                    print("Account generation failed.")
                    return
            
        if self.driver == None:
            self.start_driver()

        self.open_signup_page()

        # Wait until the element is available
        wait = WebDriverWait(self.driver, self.wait_time)
        wait_capcha = WebDriverWait(self.driver, 1000)

        element = wait.until(EC.presence_of_element_located((By.ID, "liveSwitch")))
        element.click()

        # Wait until the email input field is available
        email_input = wait.until(EC.presence_of_element_located((By.ID, ID_USERNAME)))
        login = data['email'].split('@')[0]
        self.enter_text(email_input, login)

        time.sleep(self.sleep_time)

        # Wait until the "Next" button is available and click it
        next_button = wait.until(EC.element_to_be_clickable((By.ID, ID_NEXT_BUTTON)))
        next_button.click()
        
        time.sleep(self.sleep_time)


        # Wait until the password input field is available
        password_input = wait.until(EC.presence_of_element_located((By.ID, ID_PASSWORD)))
        self.enter_text(password_input, data['password'])

        time.sleep(self.sleep_time)

        # Wait until the "Next" button is available after entering the password and click it
        next_button = wait.until(EC.element_to_be_clickable((By.ID, ID_NEXT_BUTTON)))
        next_button.click()

        # Wait until the first name input field is available
        first_name_input = wait.until(EC.presence_of_element_located((By.ID, ID_FIRST_NAME)))
        self.enter_text(first_name_input, data['first_name'])

        # Wait until the last name input field is available
        last_name_input = wait.until(EC.presence_of_element_located((By.ID, ID_LAST_NAME)))
        self.enter_text(last_name_input, data['last_name'])

        # Wait until the "Next" button is available after entering the name and click it
        next_button = wait.until(EC.element_to_be_clickable((By.ID, ID_NEXT_BUTTON)))
        next_button.click()

        dob = data['birth_date']
        if isinstance(dob, str):
            dob = datetime.strptime(dob, '%Y-%m-%d').date()
        # Wait until the birth month dropdown is available
        birth_month_select = wait.until(EC.presence_of_element_located((By.ID, ID_BIRTH_MONTH)))
        # Select a month from the dropdown
        Select(birth_month_select).select_by_value(str(dob.month))

        # Wait until the birth day dropdown is available
        birth_day_select = wait.until(EC.presence_of_element_located((By.ID, ID_BIRTH_DAY)))
        # Select a day from the dropdown
        Select(birth_day_select).select_by_value(str(dob.day))

        # Wait until the birth year input field is available
        birth_year_input = wait.until(EC.presence_of_element_located((By.ID, ID_BIRTH_YEAR)))
        # Type the birth year into the input field
        self.enter_text(birth_year_input, str(dob.year))

        # Wait until the "Next" button is available after entering the birth date and click it
        next_button = wait.until(EC.element_to_be_clickable((By.ID, ID_NEXT_BUTTON)))
        next_button.click()

        print('Waiting to solve captcha ...')

        stay_signed_in = wait_capcha.until(EC.element_to_be_clickable((By.ID, ID_ACCEPT_BUTTON)))
        stay_signed_in.click()

        print("Account successfully generated.")

        # Save the generated email and password to a file
        # Generate a unique GUID for the account
        account_id = str(uuid.uuid4())

        # Create a dictionary to store the account details
        account_details = {
            "account_id": account_id,
            "email": data['email'],
            "password": data['password'],
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "birth_date": str(dob)
        }

        return account_details

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
