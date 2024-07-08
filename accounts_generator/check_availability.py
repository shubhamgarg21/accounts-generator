from playwright.sync_api import sync_playwright

def check_email_availability(email, headless=True):
    """
    Checks the availability of an Outlook email address on the Outlook sign-up page.

    Args:
        email (str): The email address to check.
        headless (bool, optional): Whether to run the browser in headless mode. Defaults to True.

    Returns:
        bool: True if the email address is available, False otherwise.
    """
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        
        # Navigate to the Outlook sign-up page
        page.goto("https://signup.live.com/")
        
        # Fill in the email address (adjust the selector as necessary)
        page.fill("input[id='usernameInput']", email)
        
        # Click the 'Next' button to check availability (adjust the selector as necessary)
        page.click("button[id='nextButton']")
        
        #add a delay to allow the page to load
        page.wait_for_timeout(2000)

        # Wait for the response, which might include a message about the email's availability
        page.wait_for_selector("button[id='nextButton']")
        
        # Example of how to check for a specific message indicating availability
        # This is highly dependent on the website's structure and response messages
        is_available = not page.is_visible("div#usernameInputError")  # This logic may need to be adjusted
        
        # Close the browser
        browser.close()
        
        return is_available


if __name__ == "__main__":
    # Example usage
    email = "example@outlook.com"
    is_available = check_email_availability(email)
    print(f"Email {email} is {'available' if is_available else 'not available'}")