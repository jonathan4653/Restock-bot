from typing import List

from selenium.webdriver import Chrome, ChromeOptions

from .item import RestockedItem


class Scraper:
    def __init__(self, driver: Chrome):
        self.d = driver

    @staticmethod
    def get_reusable_driver():
        opts = ChromeOptions()

        # Disable images
        prefs = {"profile.managed_default_content_settings.images": 2}
        opts.add_experimental_option("prefs", prefs)

        return Chrome(options=opts)

    def get_restocked(self) -> List[RestockedItem]:
        raise NotImplementedError


class SupremeScraper(Scraper):
    def get_restocked(self):
        self.d.get('https://www.supremecommunity.com/restocks/us/1/')

        names = [i.get_attribute('innerText') for i in self.d.find_elements_by_class_name('restock-name')]
        colorways = [i.get_attribute('innerText') for i in self.d.find_elements_by_class_name('restock-colorway')]
        dts = [i.get_attribute('datetime') for i in self.d.find_elements_by_class_name('timeago')]

        items = []

        for name, colorway, dt in zip(names, colorways, dts):
            items.append(RestockedItem(name, colorway, dt))

        return items