import streamlit as st
import pdfplumber
import pandas as pd
import tempfile
import os

def read_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text

def main():
    st.title("PDFファイルビューア")

    uploaded_file = st.file_uploader("PDFファイルをアップロードしてください", type=["pdf"])

    if uploaded_file:
        # 一時ファイルをディスクに保存してからパスを取得
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name

        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        st.write(file_details)

        # PDFファイルの内容を表示
        text = read_pdf(temp_file_path)

        # テキストをDataFrameとして処理
        data = {"PDF Text": [text]}
        df = pd.DataFrame(data)

        # 罫線付きのテーブルとしてDataFrameを表示
        st.dataframe(df, height=600)

        # 一時ファイルを削除
        os.remove(temp_file_path)

if __name__ == "__main__":
    main()



# invoice_show44()

# streamlit run pdf_show02.py
