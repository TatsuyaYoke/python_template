from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Final, Literal, Optional, TypedDict, Union, cast

import pandas as pd
import pandera as pa
from pydantic import BaseModel, Field, error_wrappers

import common.settings
from common.logger import set_logger

LOGGER_IS_ACTIVE_STREAM = common.settings.logger_is_active_stream

logger = set_logger(__name__, is_active_stream=LOGGER_IS_ACTIVE_STREAM)

if getattr(sys, "frozen", False):
    p_file = Path(sys.executable)
else:
    p_file = Path(__file__).parent.parent


class AnimalRequired(TypedDict):
    name: str
    age: int


class Animal(AnimalRequired, total=False):
    height: float
    weight: float


@dataclass
class User:
    name: str
    age: int
    height: float
    weight: float

    def __post_init__(self) -> None:
        self.bmi = self.weight / (self.height / 100) ** 2


class Order(BaseModel):
    name: str
    created_at: datetime
    price: int = Field(..., gt=0)


def advanced_typing_sample() -> None:

    # TypedDict
    animal1: AnimalRequired = {"name": "dog", "age": 18}
    # {"name": "dog"} -> NG
    # {"name": "dog", "age": 18, "height": 175} -> NG
    animal2: Animal = {"name": "cat", "age": 20, "height": 60.5, "weight": 25.2}
    # {"name": "cat"} -> NG
    # {"name": "cat", "age": 20, "height": 175.5} -> OK
    logger.info(type(animal1))  # <class 'dict'>
    logger.info(type(animal2))  # <class 'dict'>

    # class
    user = User(name="yamada", age=18, height=175.2, weight=75.2)
    logger.info(f"{user.name} BMI: {user.bmi}")
    # yamada BMI: 24.499072162798946

    # cast
    # When type inference does not work and the type is Any for some reason
    any_value: Any = ["a", "b"]
    string_list = cast("list[str]", any_value)
    number_str = "1"
    number = int(number_str)
    string_int = str(number)
    logger.info(type(string_list))  # <class 'list'>
    logger.info(type(number))  # <class 'int'>
    logger.info(type(string_int))  # <class 'str'>

    # pydantic
    try:
        order = Order.parse_file(p_file / "example_external_file/order.json")
    except error_wrappers.ValidationError:
        order = None
    logger.info(order)
    # name='rice' created_at=datetime.datetime(2022, 1, 1, 0, 0) price=200

    # pandera
    df = pd.read_csv(p_file / "example_external_file/data.csv")
    schema_df = pa.DataFrameSchema(
        {
            "name": pa.Column(pa.String),
            "created_at": pa.Column(
                pa.String,
                checks=pa.Check.str_matches(r"[12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01]) ([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]"),
            ),
            "price": pa.Column(pa.Int, checks=pa.Check.gt(0)),
        }
    )
    try:
        validated_df = schema_df(df)
    except pa.errors.SchemaError:
        validated_df = None
    logger.info(validated_df)
    #     name           created_at  price
    # 0   rice  2022-01-01 00:00:00    100
    # 1  ramen  2022-01-02 00:00:00    500
    # 2   soup  2022-01-03 00:00:00    150


def basic_typing_sample() -> None:

    # Do not use Any type!!!

    # Primitive type
    item1_1: int = 1
    item2_1: float = 2.5
    item3_1: str = "string"
    item4_1: bool = True
    logger.info(type(item1_1))  # <class 'int'>
    logger.info(type(item2_1))  # <class 'float'>
    logger.info(type(item3_1))  # <class 'str>
    logger.info(type(item4_1))  # <class 'bool'>

    # You can omit writing type hints because of type inference by editor
    item1_2 = 1
    item2_2 = 2.5
    item3_2 = "string"
    item4_2 = True
    logger.info(type(item1_2))  # <class 'int'>
    logger.info(type(item2_2))  # <class 'float'>
    logger.info(type(item3_2))  # <class 'str'>
    logger.info(type(item4_2))  # <class 'bool'>

    # Optional
    item5: Optional[int] = 1
    item5 = None  # None acceptable
    logger.info(type(item5))  # <class 'NoneType'>

    # Union
    item6: Union[int, None] = 1  # Same as Optional
    item6 = None
    item7: Union[int, str] = "string"
    item7 = 1
    logger.info(type(item6))  # <class 'NoneType'>
    logger.info(type(item7))  # <class 'int'>

    # Literal
    item8: Literal["a", "b"] = "a"  # item8 = "c" -> NG
    item9: Literal[1, 2] = 2  # item9 = 3 -> NG
    logger.info(type(item8))  # <class 'str'>
    logger.info(type(item9))  # <class 'int'>

    # Final
    # Cannot change value. Final is used for constant value
    item10: Final[int] = 0  # item10 = 1 -> NG
    logger.info(type(item10))  # <class 'int'>

    # List
    list1: list[str] = ["a", "b"]  # list1.append(1) -> NG
    list2: list[int] = [1, 2, 3]  # list2.append("a") -> NG
    list3: list[int] = []  # Empty acceptable
    list4: list[Union[int, str, None]] = ["string", 2, None]
    logger.info(type(list1))  # <class 'list'>
    logger.info(type(list2))  # <class 'list'>
    logger.info(type(list3))  # <class 'list'>
    logger.info(type(list4))  # <class 'list'>

    # Tuple
    tuple1: tuple[int, int] = (1, 2)
    tuple2: tuple[int, str, list[int]] = (1, "string", [1, 2, 3])
    tuple3: tuple[str, ...] = ("a", "b", "c")  # any length acceptable
    logger.info(type(tuple1))  # <class 'tuple'>
    logger.info(type(tuple2))  # <class 'tuple'>
    logger.info(type(tuple3))  # <class 'tuple'>

    # Dict
    dict1: dict[str, int] = {"a": 1, "b": 2}
    dict2: dict[int, str] = {1: "a", 2: "b"}
    dict3: dict[str, Union[list[str], int]] = {"a": ["aaa", "bbb"], "b": 1}
    logger.info(type(dict1))  # <class 'dict'>
    logger.info(type(dict2))  # <class 'dict'>
    logger.info(type(dict3))  # <class 'dict'>


def add(x: int, y: int) -> int:
    """
    Return the result of integer addition
    Parameters
    ----------
    x : int
        addition target2
    y : int
        addition target2
    Returns
    -------
    int
        Result of integer addition
    """
    logger.debug("add")
    return x + y


def main(name: str) -> int:
    """
    Standard-output Hello {name} and return length of name

    Parameters
    ----------
    name : str
        greeting target name

    Returns
    -------
    int
        length of greeting target name
    """

    logger.info(f"Hello {name}")
    return len(name)


if __name__ == "__main__":

    name = "Python"
    name_length = main(name)
    logger.info(name_length)
    basic_typing_sample()
    advanced_typing_sample()
