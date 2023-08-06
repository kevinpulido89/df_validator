import re
from typing import Tuple

import pandas as pd


class Validator:
    """This class validates the dataframes columns"""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def validate_poc_id_column(self) -> Tuple[bool, str]:
        # Check if the column does not have null values
        if self.df["POCID"].isnull().sum() > 0:
            return False, "The column POCIDhas null values"

        # Check if the column does not have nan values
        if self.df["POCID"].isna().sum() > 0:
            return False, "The column POCID has nan values"

        # Check if the column does not have empty values
        if self.df["POCID"].empty:
            return False, "The column POCID has empty values"

        """Validates that the column poc_id has the correct values"""
        self.df["POCID"] = self.df["POCID"].astype(str)

        # Check the strings of every row are equal or greater length 6
        if not self.df["POCID"].str.len().ge(6).all():
            return False, "The column POCID has incorrect length values"

        return True, "The column POCID has the correct values"

    def validate_sku_column(self) -> Tuple[bool, str]:
        # Check if the column does not have null values
        if self.df["sku"].isnull().sum() > 0:
            return False, "The column sku has null values"

        # Check if the column does not have nan values
        if self.df["sku"].isna().sum() > 0:
            return False, "The column sku has nan values"

        # Check if the column does not have empty values
        if self.df["sku"].empty:
            return False, "The column sku has empty values"

        """Validates that the column sku has the correct values"""
        self.df["sku"] = self.df["sku"].astype(str)

        # Check the strings of every row are equal or greater length 6
        if not self.df["sku"].str.len().ge(6).all():
            return False, "The column sku has incorrect length values"

        return True, "The column sku has the correct values"

    def validate_execution_method_column(self) -> Tuple[bool, str]:
        allowed_values = ["FULL", "INCREMENTAL", "PURCHASE_MULTIPLE_VOLUME_FIXED"]

        # Check if the column does not have null values
        if self.df["execution_method"].isnull().sum() > 0:
            return False, "The column execution method has null values"

        # Check if the column does not have nan values
        if self.df["execution_method"].isna().sum() > 0:
            return False, "The column execution method has nan values"

        # Check if the column does not have empty values
        if self.df["execution_method"].empty:
            return False, "The column execution method has empty values"

        # Check if the column has the correct values
        if not self.df["execution_method"].isin(allowed_values).all():
            return False, "The column execution method has incorrect values"

        return True, "The column execution method has the correct values"

    def validate_date_format(self, row) -> bool:
        date_pattern = re.compile(r"^\d{2}-\d{2}-\d{4}$")

        if date_pattern.match(row):
            day, month, year = map(int, row.split("-"))
            if 1 <= day <= 31 and 1 <= month <= 12 and 2023 <= year <= 2030:
                return True
            else:
                return False
        else:
            return False

    def validate_start_date_column(self) -> Tuple[bool, str]:
        # Check if the column does not have null values
        if self.df["start_date"].isnull().sum() > 0:
            return False, "The column start_date has null values"

        # Check if the column does not have nan values
        if self.df["start_date"].isna().sum() > 0:
            return False, "The column start_date has nan values"

        # Check if the column does not have empty values
        if self.df["start_date"].empty:
            return False, "The column start_date has empty values"

        """Validates that the column start_date has the correct values"""
        self.df["start_date"] = self.df["start_date"].astype(str)

        # Apply the validation function to each row
        start_date_vals = self.df["start_date"].apply(lambda x: self.validate_date_format(x))

        # Check if there is any False value
        if not start_date_vals.all():
            return False, "The column start_date has incorrect date format"

        # Check the strings of every row are equal or greater length 10
        if not self.df["start_date"].str.len().ge(10).all():
            return False, "The column start_date has incorrect length values"

        return True, "The column start_date has the correct values"

    def validate_end_date_column(self) -> Tuple[bool, str]:
        # Check if the column does not have null values
        if self.df["end_date"].isnull().sum() > 0:
            return False, "The column end_date has null values"

        # Check if the column end_date does not have nan values
        if self.df["end_date"].isna().sum() > 0:
            return False, "The column end_date has nan values"

        # Check if the column end_date does not have empty values
        if self.df["end_date"].empty:
            return False, "The column end_date has empty values"

        """Validates that the column end_date has the correct values"""
        self.df["end_date"] = self.df["end_date"].astype(str)

        # Apply the validation function to each row
        end_date_vals = self.df["end_date"].apply(lambda x: self.validate_date_format(x))

        # Check if there is any False value
        if not end_date_vals.all():
            return False, "The column end_date has incorrect date format"

        # Check the strings of every row are equal or greater length 10
        if not self.df["end_date"].str.len().eq(10).all():
            return False, "The column end_date has incorrect length values"

        return True, "The column end_date has the correct values"
