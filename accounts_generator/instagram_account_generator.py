from .account_generator import AccountGenerator
from .search_mails import search_emails

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

from datetime import datetime
import time, uuid


SIGNUP_URL = 'https://www.instagram.com/accounts/emailsignup/'
ID_EMAIL = 'emailOrPhone'
ID_USERNAME = 'username'
ID_PASSWORD = 'password'
ID_FULL_NAME = 'fullName'

ID_ERROR_USERNAME = 'ssfErrorAlert'

CSS_BIRTH_MONTH = "select[title='Month:']"
CSS_BIRTH_DAY = "select[title='Day:']"
CSS_BIRTH_YEAR = "select[title='Year:']"
CSS_NEXT_BUTTON = "button[type='button']"
CSS_SUBMIT_BUTTON = "button[type='submit']"

ID_ACCEPT_BUTTON = 'acceptButton'

INSTA_CODE_SUBJECT = "is your Instagram code"


class InstagramAccountGenerator(AccountGenerator):
    def __init__(self, wait_time=2, use_proxy=True, use_user_agent=True):
        super().__init__(wait_time, use_proxy, use_user_agent)

    def open_signup_page(self):
            time.sleep(self.sleep_time)
            self.driver.get(SIGNUP_URL)

    def create_account(self, data=None):
        if data == None:
            print("No data provided.")
            print("Account generation failed.")
            return
            
        if self.driver == None:
            self.start_driver()

        self.open_signup_page()

        # Wait until the element is available
        wait = WebDriverWait(self.driver, self.wait_time)
        wait_long = WebDriverWait(self.driver, 10)

        # Fill out the registration form
        email_input     = wait.until(EC.presence_of_element_located((By.NAME, ID_EMAIL)))
        full_name_input = wait.until(EC.presence_of_element_located((By.NAME, ID_FULL_NAME)))
        username_input  = wait.until(EC.presence_of_element_located((By.NAME, ID_USERNAME)))
        password_input  = wait.until(EC.presence_of_element_located((By.NAME, ID_PASSWORD)))

        valid_username = data['username']
        full_name = data['first_name'] + ' ' + data['last_name']
        email_input.send_keys(data['email'])
        full_name_input.send_keys(full_name)
        username_input.send_keys(valid_username)
        password_input.send_keys(data['password'])

        time.sleep(self.sleep_time)

        # Find and click the "Sign up" button
        signup_button = self.driver.find_element(By.CSS_SELECTOR, CSS_SUBMIT_BUTTON)
        signup_button.click()

        # check if username is available or not by looking for element with ID ssfErrorAlert
        try:
            wait_long.until(EC.presence_of_element_located((By.ID, ID_ERROR_USERNAME)))
            if 'alternate_usernames' in data.keys():
                for username in data['alternate_usernames']:
                    print(f"Trying alternate username: {username}")
                    time.sleep(self.sleep_time)
                    username_input.clear()
                    
                    # Clear the input field using backspace
                    input_length = len(username_input.get_attribute('value'))
                    for _ in range(input_length):
                        username_input.send_keys(Keys.BACKSPACE)

                    time.sleep(self.sleep_time)
                    username_input.send_keys(username)
                    time.sleep(self.sleep_time)
                    valid_username = username
                    signup_button = self.driver.find_element(By.CSS_SELECTOR, CSS_SUBMIT_BUTTON)
                    signup_button.click()
                    time.sleep(self.sleep_time)
                    wait_long.until(EC.presence_of_element_located((By.ID, ID_ERROR_USERNAME)))

            print("Usernames not available.")
            print("Account generation failed.")
            return
        except TimeoutException:
            pass
        
        data['username'] = valid_username

        dob = data['birth_date']
        if isinstance(dob, str):
            dob = datetime.strptime(dob, '%Y-%m-%d').date()
        birth_month_select = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, CSS_BIRTH_MONTH)))
        Select(birth_month_select).select_by_value(str(dob.month))

        birth_day_select = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, CSS_BIRTH_DAY)))
        Select(birth_day_select).select_by_value(str(dob.day))

        birth_year_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, CSS_BIRTH_YEAR)))
        Select(birth_year_input).select_by_value(str(dob.year))

        # Wait until the "Next" button is available after entering the birth date and click it
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, CSS_NEXT_BUTTON)))
        next_button.click()

        # Wait for the action to complete
        time.sleep(self.sleep_time)

        # Find the element with the specified class
        popup_element = self.driver.find_element(By.CLASS_NAME, "x1cy8zhl")

        # Check if the element is present
        if popup_element:
            # Close the popup by clicking on the close button
            close_button = popup_element.find_element(By.CSS_SELECTOR, CSS_NEXT_BUTTON)
            close_button.click()
            time.sleep(self.sleep_time)
            next_button = self.driver.find_element(By.XPATH, "//button[text()='Next']")
            next_button.click()
        else:
            pass

        # Wait for the action to complete
        time.sleep(self.sleep_time)

        # Set a timeout for how long to wait for the confirmation code (in seconds)
        timeout = 300 
        start_time = time.time()
        confirmation_code = None
        while time.time() - start_time < timeout:
            # Get the confirmation code from the last message subject
            mails = search_emails(data['email'], data['password'], INSTA_CODE_SUBJECT)  # Replace with your actual username and domain

            if len(mails) > 0:
                last_subject = mails[-1]['Subject']
                # Extract the 6-digit code from the subject
                confirmation_code = last_subject.split()[0]  # Extract the first word, which is the 6-digit code
                print("Confirmation Code:", confirmation_code)
                # Now you can fill the confirmation code in the input field
                confirmation_code_input = self.driver.find_element(By.NAME, "email_confirmation_code")  
                confirmation_code_input.send_keys(confirmation_code)
                break  # Exit the loop once the confirmation code is received
            else:
                print("Confirmation code not received yet. Waiting...")
                time.sleep(10)

        # If the loop completes without finding the confirmation code
        if confirmation_code is None:
            print("Timeout: Confirmation code not received within the specified time.")
            print("Account generation failed.")
            return

        
        time.sleep(self.sleep_time)

        # Find the button element by its class name
        final_next_button = self.driver.find_element(By.CSS_SELECTOR, ".x1i10hfl.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.x972fbf.xcfux6l.x1qhh985.xm0m39n.xdl72j9.x2lah0s.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x2lwn1j.xeuugli.xexx8yu.x18d9i69.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1q0g3np.x1lku1pv.x1a2a7pz.x6s0dn4.xjyslct.x1lq5wgf.xgqcy7u.x30kzoy.x9jhf4c.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x9f619.x9bdzbf.x1ypdohk.x1f6kntn.xwhw2v2.x10w6t97.xl56j7k.x17ydfre.x1swvt13.x1pi30zi.x1n2onr6.x2b8uid.xlyipyv.x87ps6o.xcdnw81.x1i0vuye.xh8yej3.x1tu34mt.xzloghq.x3nfvp2")
        final_next_button.click()
        time.sleep(self.sleep_time)

        print("Account successfully generated.")
        
        account_details = data
        # delete a key value pair from the dictionary if it exists
        account_details.pop('alternate_usernames', None)
        account_details['insta_username'] = data['username']

        return account_details
