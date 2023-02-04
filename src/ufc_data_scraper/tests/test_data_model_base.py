from dataclasses import dataclass
from json import dumps

from ufc_data_scraper.data_models.base import DataModelBase


@dataclass(frozen=True, order=True)
class NestedDataModel(DataModelBase):
    test_nested_str: str
    test_nested_int: int


@dataclass(frozen=True, order=True)
class DataModel(DataModelBase):
    test_str: str
    test_int: int
    test_float: float
    test_nested_model: NestedDataModel


class TestDataModelBase:
    def test_as_dict(self):
        expected = {
            "test_str": "test_str",
            "test_int": 5,
            "test_float": 0.5,
            "test_nested_model": {
                "test_nested_str": "test_nested_str",
                "test_nested_int": 10,
            },
        }
        test_nested_data_model = NestedDataModel(
            test_nested_str="test_nested_str", test_nested_int=10
        )
        test_data_model = DataModel(
            test_str="test_str",
            test_int=5,
            test_float=0.5,
            test_nested_model=test_nested_data_model,
        )

        actual = test_data_model.as_dict()

        assert actual == expected

    def test_as_json(self):
        expected = {
            "test_str": "test_str",
            "test_int": 5,
            "test_float": 0.5,
            "test_nested_model": {
                "test_nested_str": "test_nested_str",
                "test_nested_int": 10,
            },
        }
        test_nested_data_model = NestedDataModel(
            test_nested_str="test_nested_str", test_nested_int=10
        )
        test_data_model = DataModel(
            test_str="test_str",
            test_int=5,
            test_float=0.5,
            test_nested_model=test_nested_data_model,
        )

        actual = test_data_model.as_json()

        assert actual == dumps(expected, default="str")
