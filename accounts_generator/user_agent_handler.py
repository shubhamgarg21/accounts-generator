import platform
from fake_headers import Headers


class UserAgentHandler:
    """
    A class that handles the generation of user agent strings based on the operating system.

    Attributes:
        OSNAME (str): The name of the operating system.

    Methods:
        __init__(): Initializes the UserAgentHandler object.
        get_user_agent(): Generates and returns a user agent string based on the operating system.
    """

    def __init__(self):
        """
        Initializes the UserAgentHandler object.

        It determines the operating system and assigns the appropriate value to the OSNAME attribute.
        """
        self.OSNAME = platform.system()
        if self.OSNAME == 'Linux':
            self.OSNAME = 'lin'
        elif self.OSNAME == 'Darwin':
            self.OSNAME = 'mac'
        elif self.OSNAME == 'Windows':
            self.OSNAME = 'win'

    def get_user_agent(self):
        """
        Generates and returns a user agent string based on the operating system.

        Returns:
            str: The generated user agent string.
        """
        header = Headers(
            browser="chrome",
            os=self.OSNAME,
            headers=False
        ).generate()
        return header['User-Agent']