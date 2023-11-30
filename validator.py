"""This module contains the class Validator, which validates the dataframes columns"""
import json
import re
from logging import warning
from typing import Tuple

import pandas as pd


class Validator:
    """Class to validate the dataframes columns

    Attributes:
        df (pd.DataFrame): The dataframe to validate
    """

    def __init__(self, df: pd.DataFrame):
        """Initialize the Validator with a DataFrame."""
        self.df = df

    def _check_null_nan_empty(self, column: pd.Series, col_name: str) -> Tuple[bool, str]:
        """Check if a column has null, nan, or empty values."""
        if column.isnull().sum() > 0:
            return False, f"The column {col_name} has null values"
        if column.isna().sum() > 0:
            return False, f"The column {col_name} has nan values"
        if column.empty:
            return False, f"The column {col_name} has empty values"
        return True, f"The column {col_name} has the correct values"

    def _check_positive_values(self, column: pd.Series, col_name: str) -> Tuple[bool, str]:
        """Check if a column has values greater than 0."""
        if not column.gt(0).all():
            return False, f"The column {col_name} has 0 or negative values"
        return True, f"The column {col_name} has the correct values"

    def _check_date_format(self, column: pd.Series, col_name: str) -> Tuple[bool, str]:
        """Check if a column has valid date format (dd-mm-yyyy)."""
        date_pattern = re.compile(
            r"^(?:(?:31(-)(?:0[13578]|1[02]))\1|(?:(?:29|30)(-)(?:0[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(-)02\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0[1-9]|1\d|2[0-8])(-)(?:(?:0[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$"
        )
        invalid_dates = column[~column.str.match(date_pattern)]

        if not invalid_dates.empty:
            return (
                False,
                f"The column {col_name} has incorrect date format: {invalid_dates.to_list()}",
            )

        valid_dates = column.str.split("-").apply(
            lambda x: 1 <= int(x[0]) <= 31 and 1 <= int(x[1]) <= 12 and 2023 <= int(x[2]) <= 2030
        )
        if not valid_dates.all():
            return False, f"The column {col_name} has invalid date values"

        return True, f"The column {col_name} has the correct values"

    def _check_list_of_strings(self, column: pd.Series, col_name: str) -> Tuple[bool, str]:
        """Check if a column contains lists of strings."""

        def is_list_of_strings(val):
            """Check if a value is a list of strings."""
            if isinstance(val, list) and all(isinstance(item, str) for item in val):
                return True
            return False

        if not column.apply(is_list_of_strings).all():
            return (
                False,
                f"The column {col_name} has incorrect values; it must be a list of strings",
            )
        return True, f"The column {col_name} has the correct values"

    def _check_allowed_values(
        self, column: pd.Series, col_name: str, allowed_values: list
    ) -> Tuple[bool, str]:
        """Check if a column has values from a list of allowed values."""
        if not column.isin(allowed_values).all():
            return False, f"The column {col_name} has incorrect values"
        return True, f"The column {col_name} has the correct values"

    def validate_poc_id_column(self) -> Tuple[bool, str]:
        """Validate the POCID column."""
        col_name = "POCID"
        result, message = self._check_null_nan_empty(self.df[col_name], col_name)
        if not result:
            return result, message

        self.df[col_name] = self.df[col_name].astype(str)
        if not self.df[col_name].str.len().ge(6).all():
            return False, f"The column {col_name} has incorrect length values"

        if self.df[col_name].duplicated().any():
            duplicated_values = self.df[self.df[col_name].duplicated()][col_name].unique()
            return (
                False,
                f"The column {col_name} has {len(duplicated_values)} duplicates: {duplicated_values}",
            )

        return True, f"The column {col_name} has the correct values"

    def validate_poc_id_and_banners_duplicates(self) -> Tuple[bool, str]:
        """Validate that the combination of POCID and banner_name columns have duplicates."""

        duplicated_values = self.df[self.df.duplicated(subset=["POCID", "banner_name"])][
            ["POCID", "banner_name"]
        ].values.tolist()

        if duplicated_values:
            return (
                False,
                f"The combination of POCID and banner_name columns has {len(duplicated_values)} duplicates",
            )

        return True, "The combination of 'POCID' & 'banner_name' dont't have duplicates"

    def validate_challenge_type_column(self) -> Tuple[bool, str]:
        """Validate the challenge_type column."""
        col_name = "challenge_type"
        allowed_values = ["EXECUTION_PTC", "CHALLENGE_VOLUME_FIXED"]
        return self._check_allowed_values(self.df[col_name], col_name, allowed_values)

    def validate_execution_method_column(self) -> Tuple[bool, str]:
        """Validate the execution_method column."""
        col_name = "execution_method"
        allowed_values = ["PURCHASE_MULTIPLE", "PURCHASE_MULTIPLE_VOLUME_FIXED"]
        return self._check_allowed_values(self.df[col_name], col_name, allowed_values)

    def validate_sku_column(self) -> Tuple[bool, str]:
        """Validate the sku column."""
        col_name = "sku"
        result, message = self._check_null_nan_empty(self.df[col_name], col_name)
        if not result:
            return result, message

        self.df[col_name] = self.df[col_name].apply(
            lambda string_sku: [str(item) for item in json.loads(string_sku)]
        )

        return self._check_list_of_strings(self.df[col_name], col_name)

    def validate_individual_target_column(self) -> Tuple[bool, str]:
        """Validate the individual_target column."""
        col_name = "individual_target"
        result, message = self._check_null_nan_empty(self.df[col_name], col_name)
        if not result:
            return result, message

        if not self.df[col_name].isin([True, False]).all():
            return False, f"The column {col_name} has incorrect values"

        return True, f"The column {col_name} has the correct values"

    def validate_null_nan_empty(self, col_name: str) -> Tuple[bool, str]:
        return self._check_null_nan_empty(self.df[col_name], col_name)

    def validate_null_nan_empty_positive(self, col_name: str) -> Tuple[bool, str]:
        result, message = self._check_null_nan_empty(self.df[col_name], col_name)
        if not result:
            return result, message

        return self._check_positive_values(self.df[col_name], col_name)

    def validate_date_column(self, col_name: str) -> Tuple[bool, str]:
        result, message = self._check_null_nan_empty(self.df[col_name], col_name)
        if not result:
            return result, message

        self.df[col_name] = self.df[col_name].astype(str)
        return self._check_date_format(self.df[col_name], col_name)


# try:
#     print("Reading CSV file")
#     df = pd.read_csv("data.csv", sep=";", encoding="utf-8")
# except (UnicodeDecodeError, FileNotFoundError):
#     print("Reading Excel file")
#     df = pd.read_excel("data.xlsx", engine="openpyxl")

# validator = Validator(df)


# def validate_and_show_result(condition: bool, message: str) -> None:
#     """Validate a condition and show the result in Streamlit"""
#     if condition:
#         print(message)
#     else:
#         warning(message)

# validate_and_show_result(*validator.validate_poc_id_column())
# validate_and_show_result(*validator.validate_poc_id_and_banners_duplicates())
# validate_and_show_result(*validator.validate_sku_column())
# validate_and_show_result(*validator.validate_challenge_type_column())
# validate_and_show_result(*validator.validate_execution_method_column())
# validate_and_show_result(*validator.validate_individual_target_column())
# validate_and_show_result(*validator.validate_date_column("start_date"))
# validate_and_show_result(*validator.validate_date_column("end_date"))
# validate_and_show_result(*validator.validate_null_nan_empty("Campaign_ID"))
# validate_and_show_result(*validator.validate_null_nan_empty("challenge_title"))
# validate_and_show_result(*validator.validate_null_nan_empty("description"))
# validate_and_show_result(*validator.validate_null_nan_empty("banner_name"))
# validate_and_show_result(*validator.validate_null_nan_empty_positive("puntos"))
# validate_and_show_result(*validator.validate_null_nan_empty_positive("META SKU"))
# validate_and_show_result(*validator.validate_null_nan_empty_positive("quantity"))
# validate_and_show_result(*validator.validate_null_nan_empty_positive("quantity_min"))
