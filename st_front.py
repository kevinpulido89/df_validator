""" Streamlit front-end for the Challenges Table Validator """
import streamlit as st
from pandas import read_csv, read_excel

from validator import Validator


def main():
    """Front Stremlit builder"""
    st.set_page_config(page_title="Challenges Table Validator", page_icon="🤖")
    st.title("Challenges Table Validator 📑🤖")

    st.warning("Remember uploading the CSV file with `;` as separator and UTF-8 encoding.")

    # Add facility to upload a dataset
    uploaded_file = st.file_uploader("💻 Load a CSV or XLSX file:", type=["xlsx", "csv"])

    if uploaded_file is not None:
        # Read in the data, add it to the list of available datasets
        try:
            file_name = uploaded_file.name[:-4]
            dataset = read_csv(uploaded_file, sep=";", encoding="utf-8")
        except UnicodeDecodeError:
            file_name = uploaded_file.name[:-5]
            dataset = read_excel(uploaded_file, engine="openpyxl")

        validator = Validator(dataset)

        def validate_and_show_result(condition: bool, message: str) -> None:
            """Validate a condition and show the result in Streamlit"""
            if condition:
                st.success(message)
            else:
                st.error(message)

        validate_and_show_result(*validator.validate_poc_id_column())
        validate_and_show_result(*validator.validate_poc_id_and_banners_duplicates())
        validate_and_show_result(*validator.validate_sku_column())
        validate_and_show_result(*validator.validate_challenge_type_column())
        validate_and_show_result(*validator.validate_execution_method_column())
        validate_and_show_result(*validator.validate_individual_target_column())
        validate_and_show_result(*validator.validate_date_column("start_date"))
        validate_and_show_result(*validator.validate_date_column("end_date"))
        validate_and_show_result(*validator.validate_null_nan_empty("Campaign_ID"))
        validate_and_show_result(*validator.validate_null_nan_empty("challenge_title"))
        validate_and_show_result(*validator.validate_null_nan_empty("description"))
        validate_and_show_result(*validator.validate_null_nan_empty("banner_name"))
        validate_and_show_result(*validator.validate_null_nan_empty_positive("puntos"))
        validate_and_show_result(*validator.validate_null_nan_empty_positive("META SKU"))
        validate_and_show_result(*validator.validate_null_nan_empty_positive("quantity"))
        validate_and_show_result(*validator.validate_null_nan_empty_positive("quantity_min"))

        st.write(f"File '{file_name}' successfully analyzed. These are 5 sample rows:")
        st.dataframe(dataset.sample(5))

    else:
        st.info("Please upload a CSV | XLSX file to get started...")
        st.stop()


if __name__ == "__main__":
    main()
