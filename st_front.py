""" Streamlit front-end for the Challenges Table Validator """
import streamlit as st
from pandas import read_csv

from validator import Validator


def main():
    """Front Stremlit builder"""
    st.set_page_config(page_title="Challenges Table Validator", page_icon="🤖")
    st.title("Challenges Table Validator 📑🤖")

    st.warning("Remember uploading the CSV file with `;` as separator and UTF-8 encoding.")

    # Add facility to upload a dataset
    uploaded_file = st.file_uploader(":computer: Load a CSV file:", type="csv")

    if uploaded_file is not None:
        # Read in the data, add it to the list of available datasets
        file_name = uploaded_file.name[:-4].capitalize()
        dataset = read_csv(uploaded_file, sep=";", encoding="utf-8")
        validator = Validator(dataset)

        b, msg = validator.validate_poc_id_column()
        if b:
            st.success(msg)
        else:
            st.error(msg)

        b, msg = validator.validate_meta_sku_column()
        if b:
            st.success(msg)
        else:
            st.error(msg)

        b, msg = validator.validate_points_column()
        if b:
            st.success(msg)
        else:
            st.error(msg)

        b, msg = validator.validate_campaign_id_column()
        if b:
            st.success(msg)
        else:
            st.error(msg)

        b, msg = validator.validate_challenge_type_column()
        if b:
            st.success(msg)
        else:
            st.error(msg)

        b, msg = validator.validate_execution_method_column()
        if b:
            st.success(msg)
        else:
            st.error(msg)

        b, msg = validator.validate_sku_column()
        if b:
            st.success(msg)
        else:
            st.error(msg)

        b, msg = validator.validate_start_date_column()
        if b:
            st.success(msg)
        else:
            st.error(msg)

        b, msg = validator.validate_end_date_column()
        if b:
            st.success(msg)
        else:
            st.error(msg)

        b, msg = validator.validate_individual_target_column()
        if b:
            st.success(msg)
        else:
            st.error(msg)

        b, msg = validator.validate_challenge_title_column()
        if b:
            st.success(msg)
        else:
            st.error(msg)

        b, msg = validator.validate_description_column()
        if b:
            st.success(msg)
        else:
            st.error(msg)

        b, msg = validator.validate_banner_name_column()
        if b:
            st.success(msg)
        else:
            st.error(msg)

        b, msg = validator.validate_quantity_columns()
        if b:
            st.success(msg)
        else:
            st.error(msg)

        b, msg = validator.validate_quantity_min_columns()
        if b:
            st.success(msg)
        else:
            st.error(msg)

        st.write(f"File '{file_name}' successfully analyzed. These are 5 sample rows:")
        st.dataframe(dataset.sample(5))

    else:
        st.info("Please upload a CSV file to get started.")
        st.stop()


if __name__ == "__main__":
    main()
