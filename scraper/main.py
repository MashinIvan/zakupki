from helpers import progress, sleeper, scroll_into_view
from config import config

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver

from urllib.parse import urlparse, parse_qs

from datetime import datetime
import dateutil.parser
import dataclasses
import logging
import typing
import os
import re


logger = logging.getLogger('scraper')


@dataclasses.dataclass
class Request:
    request_number: int = None
    request_name: datetime = None
    request_admit_sign: str = None


@dataclasses.dataclass
class Protocol:
    protocol_number: str = None
    protocol_url: str = None

    requests: typing.List[Request] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class DataUnitModel:
    number: str = None
    url: str = None

    starting_price: float = None
    posted: datetime = None
    updated: datetime = None
    ends: datetime = None

    protocols: typing.List[Protocol] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class Scraper:
    url: str
    limit: int
    headless: bool

    driver: WebDriver = None

    total: int = 0
    _visited: int = 0
    data: typing.List[DataUnitModel] = dataclasses.field(default_factory=list)

    _stop: bool = False

    def __post_init__(self):
        options = webdriver.ChromeOptions()
        options.headless = self.headless
        options.add_argument("--log-level=3")

        self.driver = webdriver.Chrome(
            executable_path=os.path.join(config.root, 'storage/drivers/chromedriver.exe'),
            options=options
        )
        logger.info("Driver set")

    def run(self) -> typing.List[DataUnitModel]:
        while not self._stop:
            self._switch_tab(1)
            self.driver.get(self.url.strip())
            self._set_total()

            sleeper.short()
            logger.info('Got to page {}'.format(self._page_number))

            try:
                self.scrap_page()
            except:
                self._next_page()
                continue

            logger.info('Su {}'.format(self._page_number))

            self._next_page()

        self.driver.close()
        return self.data

    @progress
    def scrap_page(self):
        cards = self.driver.find_elements_by_class_name("search-registry-entry-block")
        if len(cards) == 0:
            self._stop = True
            return

        for card in cards:
            if self._visited > self.total:
                self._stop = True
                return
            result = self._scrap_card(card)
            self._visited += 1
            if result:
                self.data.append(self._scrap_card(card))
            yield 1

    def _scrap_card(self, card: WebElement) -> typing.Union[DataUnitModel, None]:
        try:
            links = card.find_elements_by_tag_name('a')
            url = next(filter(
                lambda x: "№" in x.text,
                links
            ))
            number = re.search(r'(№\s.*)', url.text).group(1)

            href = url.get_attribute('href')
            self._switch_tab(2)
            self.driver.get(href)
            sleeper.medium()

            starting_price_element: WebElement = self.driver.find_elements_by_xpath('//div[@class="price"]/span')[1]
            starting_price = re.sub(r'\D', '', starting_price_element.text.split(',')[0])

            posted_parent_element: WebElement = self.driver.find_element_by_xpath(
                '//div[child::span[contains(text(), "Размещено")]]')
            posted = None
            if posted_parent_element and len(posted_parent_element.find_elements_by_tag_name('span')) > 1:
                posted = dateutil.parser.parse(
                    posted_parent_element.find_elements_by_tag_name('span')[1].text.strip(), dayfirst=True)

            updated_parent_element: WebElement = self.driver.find_element_by_xpath(
                '//div[child::span[contains(text(), "Обновлено")]]')
            updated = None
            if updated_parent_element and len(updated_parent_element.find_elements_by_tag_name('span')) > 1:
                updated = dateutil.parser.parse(
                    updated_parent_element.find_elements_by_tag_name('span')[1].text.strip(), dayfirst=True)

            ends_parent_element: WebElement = self.driver.find_element_by_xpath(
                '//div[child::span[contains(text(), "Окончание подачи заявок")]]')
            ends = None
            if ends_parent_element and len(ends_parent_element.find_elements_by_tag_name('span')) > 1:
                ends = dateutil.parser.parse(
                    ends_parent_element.find_elements_by_tag_name('span')[1].text.strip(), dayfirst=True)

            documents_element = self.driver.find_element_by_xpath(
                '//div[@class="cardHeaderBlock"]//a[contains(text(),"Документы")]')
            scroll_into_view(self.driver, documents_element)
            documents_element.click()
            sleeper.short()

            protocols = list(self._scrap_protocols())

            self._switch_tab(1)

            return DataUnitModel(
                number=number,
                url=href,

                starting_price=float(starting_price),
                posted=posted,
                updated=updated,
                ends=ends,

                protocols=protocols,
            )
        except:
            return

    def _scrap_protocols(self) -> typing.List[Protocol]:
        try:
            protocols_parent_element = self.driver.find_element_by_xpath(
                '//div/*[self::h1 or self::h2 or self::h3][contains(text(), "Протоколы")]/..')

            for protocol_element in protocols_parent_element.find_elements_by_xpath('div'):
                protocol_number = re.search(r'(№\S+)',
                                            protocol_element.find_element_by_tag_name('a').text).group(1)
                protocol_url = protocol_element.find_element_by_tag_name('a').get_attribute('href')

                requests_data = list(self._scrap_requests(protocol_url))

                yield Protocol(
                    protocol_number=protocol_number,
                    protocol_url=protocol_url,

                    requests=requests_data,
                )
        except:
            pass

    def _scrap_requests(self, protocol_url: str) -> typing.List[Request]:
        try:
            self._switch_tab(3)
            self.driver.get(protocol_url)
            sleeper.short()

            try:
                requests_url = self.driver.find_element_by_xpath(
                    '//a[contains(text(), "Список заявок")]').get_attribute('href')
            except NoSuchElementException:
                requests_url = None

            if requests_url:
                self.driver.get(requests_url)

                request_elements = self.driver.find_elements_by_xpath('//table/tbody/tr')[1::2]

                for i, item in enumerate(request_elements):
                    request_name = item.find_elements_by_tag_name('td')[2].text.strip()
                    request_admit_sign = item.find_elements_by_tag_name('td')[3].text.strip()

                    yield Request(
                        request_number=i + 1,
                        request_name=request_name,
                        request_admit_sign=request_admit_sign,
                    )

            self._switch_tab(2)
        except:
            self._switch_tab(2)

    def _next_page(self) -> None:
        url = re.sub(
            r'pageNumber=(\d+)&',
            "pageNumber={}&".format(int(self._page_number) + 1),
            self.url,
        )
        self.url = url

    def _set_total(self):
        if self.total == 0:
            try:
                total_element = self.driver.find_element_by_class_name('search-results__total')
            except NoSuchElementException:
                return self.limit
            total = int(re.sub(r'\D', '', total_element.text))
            self.total = total if total < self.limit else self.limit

    @property
    def _page_number(self):
        query = urlparse(self.url).query
        page = parse_qs(query).get("pageNumber", 1)
        if isinstance(page, list):
            return int(page[0])
        return page

    def _switch_tab(self, tab_number: int) -> None:
        try:
            self.driver.switch_to.window(self.driver.window_handles[tab_number - 1])
        except IndexError:
            for i in range(tab_number - len(self.driver.window_handles)):
                self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[tab_number - 1])
