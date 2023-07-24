import streamlit as st
import base64
import os

def invoice_show44():
    st.title("PDF Viewer")
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if pdf_file is not None:
        # 一時的なファイルにPDFデータを書き込む
        with open("temp.pdf", "wb") as f:
            f.write(pdf_file.read())

        # 一時的なファイルをBase64エンコードしてHTMLタグに埋め込む
        with open("temp.pdf", "rb") as f:
            pdf_base64 = base64.b64encode(f.read()).decode("utf-8")
            pdf_embed = f'<embed src="data:application/pdf;base64,{pdf_base64}" width="100%" height="600px" type="application/pdf">'
            st.markdown(pdf_embed, unsafe_allow_html=True)

        # 一時的なファイルを削除
        os.remove("temp.pdf")

invoice_show44()

# streamlit run pdf_show04.py
