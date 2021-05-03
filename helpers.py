from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver

import typing
import random
import time


def scroll_into_view(driver: WebDriver, element: WebElement) -> None:
    driver.execute_script("arguments[0].scrollIntoView();", element)


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
        current = 0

        print(
            format_.format(
                done="#" * 0,
                do=" " * length,
                percent=0,
            ),
            end="\r"
        )
        try:
            while True:
                value = next(func(self, *args, **kwargs))

                current += value
                total = self.total
                percent = current / total
                percent = 1 if percent > 1 else percent
                n_fill = int(percent * length)
                n_empty = length - n_fill

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
