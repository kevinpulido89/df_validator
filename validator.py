"""This module contains the class Validator, which validates the dataframes columns"""
import json
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

    def validate_meta_sku_column(self) -> Tuple[bool, str]:
        # Check if the column does not have null values
        if self.df["META SKU"].isnull().sum() > 0:
            return False, "The column META SKU has null values"

        # Check if the column does not have nan values
        if self.df["META SKU"].isna().sum() > 0:
            return False, "The column META SKU has nan values"

        # Check if the column does not have empty values
        if self.df["META SKU"].empty:
            return False, "The column META SKU has empty values"

        # Check if the column has greater than 0 values
        if not self.df["META SKU"].gt(0).all():
            return False, "The column META SKU has 0 or negative values"

    def validate_points_column(self) -> Tuple[bool, str]:
        # Check if the column does not have null values
        if self.df["puntos"].isnull().sum() > 0:
            return False, "The column points has null values"

        # Check if the column does not have nan values
        if self.df["puntos"].isna().sum() > 0:
            return False, "The column points has nan values"

        # Check if the column does not have empty values
        if self.df["puntos"].empty:
            return False, "The column points has empty values"

        # Check if the column has greater than 0 values
        if not self.df["puntos"].gt(0).all():
            return False, "The column points has 0 or negative values"

    def validate_campaign_id_column(self) -> Tuple[bool, str]:
        # Check if the column does not have null values
        if self.df["Campaign_ID"].isnull().sum() > 0:
            return False, "The column Campaign_ID has null values"

        # Check if the column does not have nan values
        if self.df["Campaign_ID"].isna().sum() > 0:
            return False, "The column Campaign_ID has nan values"

        # Check if the column does not have empty values
        if self.df["Campaign_ID"].empty:
            return False, "The column Campaign_ID has empty values"

    def validate_challenge_type_column(self) -> Tuple[bool, str]:
        allowed_values = ["EXECUTION_PTC", "CHALLENGE_VOLUME_FIXED"]

        # Check if the column does not have null values
        if self.df["challenge_type"].isnull().sum() > 0:
            return False, "The column challenge_type has null values"

        # Check if the column does not have nan values
        if self.df["challenge_type"].isna().sum() > 0:
            return False, "The column challenge_type has nan values"

        # Check if the column does not have empty values
        if self.df["challenge_type"].empty:
            return False, "The column challenge_type has empty values"

        # Check if the column has the correct values
        if not self.df["challenge_type"].isin(allowed_values).all():
            return False, "The column challenge_type has incorrect values"

        return True, "The column challenge_type has the correct values"

    def validate_execution_method_column(self) -> Tuple[bool, str]:
        allowed_values = ["PURCHASE_MULTIPLE", "PURCHASE_MULTIPLE_VOLUME_FIXED"]

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

        self.df["sku"] = self.df["sku"].apply(lambda string_sku: [str(item) for item in json.loads(string_sku)])

        # Check if the column has list with strings
        if not self.df.sku.apply(lambda x: isinstance(x, list) and all(isinstance(y, str) for y in x)).all():
            return False, "The column sku has incorrect values; it must be a list of strings"

        return True, "The column sku has the correct values"

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

        # Check the strings of every row are equal to length 10
        if not self.df["start_date"].str.len().eq(10).all():
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

        # Check the strings of every row are equal length 10
        if not self.df["end_date"].str.len().eq(10).all():
            return False, "The column end_date has incorrect length values"

        return True, "The column end_date has the correct values"

    def validate_individual_target_column(self) -> Tuple[bool, str]:
        # Check if the column does not have null values
        if self.df["individual_target"].isnull().sum() > 0:
            return False, "The column individual_target has null values"

        # Check if the column does not have nan values
        if self.df["individual_target"].isna().sum() > 0:
            return False, "The column individual_target has nan values"

        # Check if the column does not have empty values
        if self.df["individual_target"].empty:
            return False, "The column individual_target has empty values"

        # Check if the column has only True or False values
        if not self.df["individual_target"].isin([True, False]).all():
            return False, "The column individual_target has incorrect values"

    def validate_challenge_title_column(self) -> Tuple[bool, str]:
        # Check if the column does not have null values
        if self.df["challenge_title"].isnull().sum() > 0:
            return False, "The column challenge_title has null values"

        # Check if the column does not have nan values
        if self.df["challenge_title"].isna().sum() > 0:
            return False, "The column challenge_title has nan values"

        # Check if the column does not have empty values
        if self.df["challenge_title"].empty:
            return False, "The column challenge_title has empty values"

    def validate_description_column(self) -> Tuple[bool, str]:
        # Check if the column does not have null values
        if self.df["description"].isnull().sum() > 0:
            return False, "The column description has null values"

        # Check if the column does not have nan values
        if self.df["description"].isna().sum() > 0:
            return False, "The column description has nan values"

        # Check if the column does not have empty values
        if self.df["description"].empty:
            return False, "The column description has empty values"

    def validate_banner_name_column(self) -> Tuple[bool, str]:
        # Check if the column does not have null values
        if self.df["banner_name"].isnull().sum() > 0:
            return False, "The column banner_name has null values"

        # Check if the column does not have nan values
        if self.df["banner_name"].isna().sum() > 0:
            return False, "The column banner_name has nan values"

        # Check if the column does not have empty values
        if self.df["banner_name"].empty:
            return False, "The column banner_name has empty values"

    def validate_quantity_columns(self) -> Tuple[bool, str]:
        # Check if the column does not have null values
        if self.df["quantity"].isnull().sum() > 0:
            return False, "The column quantity has null values"

        # Check if the column does not have nan values
        if self.df["quantity"].isna().sum() > 0:
            return False, "The column quantity has nan values"

        # Check if the column does not have empty values
        if self.df["quantity"].empty:
            return False, "The column quantity has empty values"

        # Check if the column has greater than 0 values
        if not self.df["quantity"].gt(0).all():
            return False, "The column quantity has 0 or negative values"

    def validate_quantity_min_columns(self) -> Tuple[bool, str]:
        # Check if the column does not have null values
        if self.df["quantity_min"].isnull().sum() > 0:
            return False, "The column quantity_min has null values"

        # Check if the column does not have nan values
        if self.df["quantity_min"].isna().sum() > 0:
            return False, "The column quantity_min has nan values"

        # Check if the column does not have empty values
        if self.df["quantity_min"].empty:
            return False, "The column quantity_min has empty values"

        # Check if the column has greater than 0 values
        if not self.df["quantity_min"].gt(0).all():
            return False, "The column quantity_min has 0 or negative values"
