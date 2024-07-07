import requests
from lxml.html import fromstring
from random import shuffle, choice
from fake_headers import Headers

class ProxyGenerator:
    """
    A class for generating and retrieving valid proxies from sslproxies.org.
    """

    def __init__(self):
        self.proxies_list = []
        self.fetch_proxies()

    def fetch_proxies(self):
        """
        Fetches a list of proxies from sslproxies.org and updates the cached list.

        Returns:
            list: A list of valid proxies.
        """
        url = 'https://sslproxies.org/'
        response = requests.get(url)
        parser = fromstring(response.text)
        self.proxies_list = []
        for i in parser.xpath('//tbody/tr')[:100]:
            if i.xpath('.//td[7][contains(text(),"yes")]'):
                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                self.proxies_list.append(proxy)
        shuffle(self.proxies_list)
        return self.proxies_list

    def update_proxies(self):
        """
        Updates the list of proxies by fetching new proxies from sslproxies.org.

        Returns:
            list: A list of valid proxies.
        """
        self.fetch_proxies()

    def get_valid_proxy(self):
        """
        Retrieves a valid proxy from the list of proxies.

        Returns:
            str: A valid proxy.
        """
        header = Headers(
            headers=False
        ).generate()
        agent = header['User-Agent']

        headers = {
            'User-Agent': f'{agent}',
        }

        url = 'http://icanhazip.com'
        while True:
            proxy = choice(self.proxies_list)
            proxies = {
                'http': f'http://{proxy}',
                'https': f'https://{proxy}',
            }
            try:
                response = requests.get(url, headers=headers, proxies=proxies, timeout=1)
                if response.status_code == 200:
                    return proxy
            except:
                continue

    def generate_proxy(self):
        """
        Generates a valid proxy using the cached proxies and updates the list only when no cached proxy is valid.

        Returns:
            str: A valid proxy.
        """
        proxy = self.get_valid_proxy()
        if not proxy:
            self.update_proxies()
            proxy = self.get_valid_proxy()
        return proxy
