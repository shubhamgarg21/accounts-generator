from selenium import webdriver

class ChromeDriver:
    def __init__(self, headless=False, proxy=None, user_agent=None, extension=None, stealth_mode=False):
        self.headless = headless
        self.proxy = proxy
        self.user_agent = user_agent
        self.extension = extension
        self.stealth_mode = stealth_mode

    def prepare_driver(self):
        """
        Prepare and return a WebDriver instance with the specified options.

        Returns:
            WebDriver: An instance of the Chrome WebDriver with the specified options.
        """
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument('--headless')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-web-security')
        options.add_argument('--no-sandbox')
        options.add_argument('--log-level=3')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        if self.user_agent:
            options.add_argument(f'--user-agent={self.user_agent}')
        if self.proxy:
            options.add_argument(f'--proxy-server=http://{self.proxy}')
        if self.extension:
            options.add_extension(self.extension)
        
        driver = webdriver.Chrome(options=options)

        driver.delete_all_cookies()

        if self.stealth_mode:
            from selenium_stealth import stealth
            stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
            )

        return driver

