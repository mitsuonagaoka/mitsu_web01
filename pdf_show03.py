import streamlit as st
import fitz  # PyMuPDFをインポート
from PIL import Image
import tempfile
import os

def pdf_to_images(file_path):
    images = []
    with fitz.open(file_path) as pdf_document:
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            image_list = page.get_pixmap()
            img = Image.frombytes("RGB", [image_list.width, image_list.height], image_list.samples)
            images.append(img)
    return images

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

        # PDFを画像に変換
        images = pdf_to_images(temp_file_path)

        # 画像を表示
        for image in images:
            st.image(image, use_column_width=True)

        # 一時ファイルを削除
        os.remove(temp_file_path)

if __name__ == "__main__":
    main()



# invoice_show44()

# streamlit run pdf_show03.py
