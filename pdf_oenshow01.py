import streamlit as st
from pdf2image import convert_from_path
import tempfile
import os


def invoice_show44():
    st.title("PDFファイルビューア")

    uploaded_file = st.file_uploader("PDFファイルをアップロードしてください", type=["pdf"])

    if uploaded_file:
        # 一時ファイルをディスクに保存してからパスを取得
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name

        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        st.write(file_details)

        # PDFを画像に変換
        images = convert_from_path(temp_file_path)

        # 画像を表示
        for image in images:
            st.image(image, use_column_width=True)

        # 一時ファイルを削除
        os.remove(temp_file_path)

invoice_show44()


# if __name__ == "__main__":
#     main()

# streamlit run pdf_oenshow01.py
