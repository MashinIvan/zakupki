import pandas as pd
import fire

from scraper.main import Scraper

import dataclasses
import logging
import typing


logger = logging.getLogger(__name__)


class Runner:
    _headless: bool = False

    def scrap(self, limit: int = 10000) -> None:
        url = input('url: ')
        scraper: Scraper = Scraper(url=url, limit=limit, headless=self._headless)
        data = scraper.run()
        self.save(data)

    def scrap_headless(self, *args, **kwargs):
        self._headless = True
        self.scrap(*args, **kwargs)

    def save(self, data):
        rows = []

        for data_unit in data:
            data_unit_json = dataclasses.asdict(data_unit)
            protocols: typing.List[dict] = data_unit_json.pop('protocols')

            for protocol_json in protocols:
                requests_: typing.List[dict] = protocol_json.pop('requests')

                for request_json in requests_:
                    rows.append(
                        {**data_unit_json, **protocol_json, **request_json}
                    )

        data_frame = pd.DataFrame(rows)
        data_frame.to_csv('storage/data.csv', sep=';')


if __name__ == "__main__":
    fire.Fire(Runner)
