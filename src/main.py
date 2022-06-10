import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import (
    Any,
    Dict,
    Final,
    List,
    Literal,
    Optional,
    Tuple,
    TypedDict,
    Union,
    cast,
)

import pandas as pd
import pandera as pa
from pydantic import BaseModel, Field, error_wrappers

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
    print(type(animal1), type(animal2))
    # <class 'dict'> <class 'dict'>

    # class
    user = User(name="yamada", age=18, height=175.2, weight=75.2)
    print(f"{user.name} BMI: {user.bmi}")
    # yamada BMI: 24.499072162798946

    # cast
    # When type inference does not work and the type is Any for some reason
    any_value: Any = ["a", "b"]
    string_list = cast(List[str], any_value)
    number_str = "1"
    number = int(number_str)
    string_int = str(number)
    print(type(string_list), type(number), type(string_int))
    # <class 'list'> <class 'int'> <class 'str'>

    # pydantic
    try:
        order = Order.parse_file(p_file / "example_external_file/order.json")
    except error_wrappers.ValidationError:
        order = None
    print(order)
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
    print(validated_df)
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
    print(type(item1_1), type(item2_1), type(item3_1), type(item4_1))
    # <class 'int'> <class 'float'> <class 'str'> <class 'bool'>

    # You can omit writing type hints because of type inference by editor
    item1_2 = 1
    item2_2 = 2.5
    item3_2 = "string"
    item4_2 = True
    print(type(item1_2), type(item2_2), type(item3_2), type(item4_2))
    # <class 'int'> <class 'float'> <class 'str'> <class 'bool'>

    # Optional
    item5: Optional[int] = 1
    item5 = None  # None acceptable
    print(type(item5))
    # <class 'NoneType'>

    # Union
    item6: Union[int, None] = 1  # Same as Optional
    item6 = None
    item7: Union[int, str] = "string"
    item7 = 1
    print(type(item6), type(item7))
    # <class 'NoneType'> <class 'int'>

    # Literal
    item8: Literal["a", "b"] = "a"  # item8 = "c" -> NG
    item9: Literal[1, 2] = 2  # item9 = 3 -> NG
    print(type(item8), type(item9))
    # <class 'str'> <class 'int'>

    # Final
    # Cannot change value. Final is used for constant value
    item10: Final[int] = 0  # item10 = 1 -> NG
    print(type(item10))
    # <class 'int'>

    # List
    # List is used in python 3.6 to 3.8 instead of list which is used in python 3.9 or more
    list1: List[str] = ["a", "b"]  # list1.append(1) -> NG
    list2: List[int] = [1, 2, 3]  # list2.append("a") -> NG
    list3: List[int] = []  # Empty acceptable
    list4: List[Union[int, str, None]] = ["string", 2, None]
    print(type(list1), type(list2), type(list3), type(list4))
    # <class 'list'> <class 'list'> <class 'list'> <class 'list'>

    # Tuple
    # Tuple is used in python 3.6 to 3.8 instead of tuple which is used in python 3.9 or more
    tuple1: Tuple[int, int] = (1, 2)
    tuple2: Tuple[int, str, List[int]] = (1, "string", [1, 2, 3])
    tuple3: Tuple[str, ...] = ("a", "b", "c")  # any length acceptable
    print(type(tuple1), type(tuple2), type(tuple3))
    # <class 'tuple'> <class 'tuple'> <class 'tuple'>

    # Dict
    # Dict is used in python 3.6 to 3.8 instead of dict which is used in python 3.9 or more
    dict1: Dict[str, int] = {"a": 1, "b": 2}
    dict2: Dict[int, str] = {1: "a", 2: "b"}
    dict3: Dict[str, Union[List[str], int]] = {"a": ["aaa", "bbb"], "b": 1}
    print(type(dict1), type(dict2), type(dict3))
    # <class 'dict'> <class 'dict'> <class 'dict'>


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

    print(f"Hello {name}")
    return len(name)


if __name__ == "__main__":

    name = "Python"
    name_length = main(name)
    print(name_length)
    basic_typing_sample()
    advanced_typing_sample()
