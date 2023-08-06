import pandas as pd
import streamlit as st

from validator import Validator


def main():
    st.set_page_config(page_title="Challenges Table Validator", page_icon="🤖")
    st.title("Challenges Table Validator 📑🤖")

    # Add facility to upload a dataset
    uploaded_file = st.file_uploader(":computer: Load a CSV file:", type="csv")

    if uploaded_file is not None:
        # Read in the data, add it to the list of available datasets
        file_name = uploaded_file.name[:-4].capitalize()
        dataset = pd.read_csv(uploaded_file, sep=";", encoding="utf-8")
        validator = Validator(dataset)

        b, msg = validator.validate_poc_id_column()
        if b:
            st.success(msg)
        else:
            st.error(msg)

        b, msg = validator.validate_sku_column()
        if b:
            st.success(msg)
        else:
            st.error(msg)

        b, msg = validator.validate_execution_method_column()
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

        st.write(f"File '{file_name}' successfully uploaded. These are the first 3 rows:")
        st.write(dataset.head(3))

    else:
        st.info("Please upload a CSV file to get started.")
        st.stop()


if __name__ == "__main__":
    main()
