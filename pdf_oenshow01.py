import streamlit as st
import base64

def invoice_show44():
    st.title("PDF Viewer")
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if pdf_file is not None:
        # PDFファイルをBase64エンコードしてHTMLタグに埋め込む
        pdf_base64 = base64.b64encode(pdf_file.read()).decode("utf-8")
        pdf_embed = f'<embed src="data:application/pdf;base64,{pdf_base64}" width="100%" height="600px" type="application/pdf">'
        st.markdown(pdf_embed, unsafe_allow_html=True)

invoice_show44()

# streamlit run pdf_oenshow01.py
