import streamlit as st
import base64
import os

def main():
    st.title("PDF Viewer")
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    # PDFファイルのディレクトリパス
    pdf_directory = r"C:\Users\marom\Invoice"

    # PDFファイルの一覧を取得する
    pdf_files = os.listdir(pdf_directory)

    # PDFファイルを新しい順にソートする
    pdf_files.sort(key=lambda x: os.path.getmtime(os.path.join(pdf_directory, x)), reverse=True)

    # 選択ボックスにPDFファイルを表示する
    selected_pdf = st.selectbox("Select PDF", pdf_files)

    # PDFファイルのパス
    pdf_path = os.path.join(pdf_directory, selected_pdf)

    # # PDFを画像に変換する
    # images = convert_from_path(pdf_path)

    if pdf_file is not None:
        # PDFファイルをBase64エンコードしてHTMLタグに埋め込む
        pdf_base64 = base64.b64encode(pdf_file.read()).decode("utf-8")
        pdf_embed = f'<embed src="data:application/pdf;base64,{pdf_base64}" width="100%" height="600px" type="application/pdf">'
        st.markdown(pdf_embed, unsafe_allow_html=True)

if __name__ == "__main__":
    main()




# streamlit run pdf_show02.py
