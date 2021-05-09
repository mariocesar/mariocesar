from typing import Generator, Any, Union, List
from functools import wraps
from itertools import chain
from pathlib import Path
from dataclasses import dataclass


RootDir = Path(__file__).parent


def consumer(func):
    @wraps(func)
    def wrapper(*args, **kw):
        gen = func(*args, **kw)
        next(gen)
        return gen

    return wrapper


def src(patterns: Union[str, List[str]]) -> Generator[Path, Path, None]:
    if isinstance(patterns, str):
        patterns = [patterns]

    print(f"{patterns=}")

    for pattern in patterns:
        yield from RootDir.glob(pattern)


def puts():
    def inner(record: Path):
        print(f"{record=}")
        return record

    return inner


def exhausts(generator: Generator[Any, Any, Any]) -> None:
    for item in generator:
        pass


if __name__ == "__main__":
    exhausts(map(puts(), src(["README.md", "pages/**/*.js"])))
