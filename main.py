from base import Scraper

import logging
import fire
import sys


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs.log", mode="w"),
    ],
)

logger = logging.getLogger(__name__)


class Runner:
    def scrap(self, url: str, limit: int = 10000) -> None:
        scraper: Scraper = Scraper(url=url, limit=limit)
        scraper.run()
        # try:
        #     scraper.run()
        # except KeyboardInterrupt:
        #     return
        # except Exception as e:
        #     logger.error(e)
        #     return


if __name__ == "__main__":
    fire.Fire(Runner)
