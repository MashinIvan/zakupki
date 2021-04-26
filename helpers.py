from bs4 import BeautifulSoup as bs

from functools import wraps
import typing
import random
import time


def find_links(soup: bs, options: dict = None) -> list:
    if not options:
        options = {}
    links = soup.find_all("a", **options)

    return links


class sleeper:
    @classmethod
    def short(cls) -> None:
        """interval: [0.2, 1.5]"""
        from_ = 0.2
        to_ = 1.5

        rnd = random.random()
        time.sleep(rnd * (to_ - from_) + from_)

    @classmethod
    def medium(cls) -> None:
        """interval: [1.5, 3]"""
        from_ = 1.5
        to_ = 3

        rnd = random.random()
        time.sleep(rnd * (to_ - from_) + from_)

    @classmethod
    def medium_long(cls) -> None:
        """interval: [3.5, 5]"""
        from_ = 3.5
        to_ = 5

        rnd = random.random()
        time.sleep(rnd * (to_ - from_) + from_)

    @classmethod
    def long(cls) -> None:
        """interval: [5, 6.5]"""
        from_ = 5
        to_ = 6.5

        rnd = random.random()
        time.sleep(rnd * (to_ - from_) + from_)


def progress(func: typing.Generator[int, typing.Any, typing.Any]) -> typing.Callable:
    format_: str = "[{done}{do}] {percent:.2f}%"
    length: int = 30

    def wrapper(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        total = self._total
        current = 1

        print(
            format_.format(
                done="#" * 0,
                do=" " * length,
                percent=0,
            )
        )
        try:
            while True:
                value = next(func(self, *args, **kwargs))

                percent = current / total
                n_fill = int(percent * length)
                n_empty = length - n_fill

                current += value
                print(
                    format_.format(
                        done="#" * n_fill,
                        do=" " * n_empty,
                        percent=percent * 100,
                    ),
                    end="\r",
                )
        except StopIteration as result:
            print(
                format_.format(
                    done="#" * length,
                    do=" " * 0,
                    percent=100,
                )
            )
            return result.value

    return wrapper
