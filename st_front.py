import streamlit as st
import pandas as pd


def main():
    st.set_page_config(page_title="Challenges Table Validator", page_icon="🤖")
    st.title("Challenges Table Validator 📚🤖")

    st.write("This app analyzes the sentiment of your text")

    # Add facility to upload a dataset
    uploaded_file = st.file_uploader(":computer: Load a CSV file:", type="csv")

    if uploaded_file is not None:
        # Read in the data, add it to the list of available datasets
        file_name = uploaded_file.name[:-4].capitalize()
        dataset = pd.read_csv(uploaded_file, sep=";", encoding="utf-8")
        st.write(dataset)
        st.success(f"File {file_name} successfully uploaded.")

        st.write("## Select the column with the text to analyze")
        text_column = st.selectbox("Select the column with the text to analyze", dataset.columns)
        st.write(f"Selected column: {text_column}")

    else:
        st.info("Please upload a CSV file to get started.")
        st.stop()


if __name__ == "__main__":
    main()
