from helpers import progress

from bs4 import BeautifulSoup as bs
from pydantic import BaseModel
import dataclasses
import requests
import typing
import re


class DataUnitModel(BaseModel):
    one: str
    two: int


@dataclasses.dataclass
class Scraper:
    url: str
    limit: int

    _total: int = 0
    _data: list = dataclasses.field(default_factory=list)

    _stop: bool = False

    @progress
    def run(self) -> typing.List[DataUnitModel]:
        while not self._finished():
            resp = requests.get(self.url.strip())
            soup = bs(resp.text, "lxml")

            data = self.scrap_page(soup)
            self._data += data
            yield len(data)

        return self._data

    def scrap_page(self, soup: bs) -> typing.List[DataUnitModel]:
        cards = soup.find_all("div", {"class": "search-registry-entry-block box-shadow-search-input"})
        if len(cards) == 0:
            this._stop = True
            return []

        data = []
        for card in cards:
            data.append(self._scrap_card(card))

        return []

    def _scrap_card(self) -> DataUnitModel:
        return {}

    def _finished(self) -> bool:
        return self._total >= self.limit or self._stop
