import streamlit as st
from pdf2image import convert_from_path
# from reportlab.pdfbase.ttfonts import TTFont
import pytesseract
import os

# pip show pdf2image'pdf2image'があれば、モジュールの情報が表示されます。/なければ、Package(s) not found: pdf2image

def invoice_show44():
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

    # PDFを画像に変換する
    images = convert_from_path(pdf_path)

    # 画像を表示する
    for i, image in enumerate(images):
        st.image(image, caption=f"Page {i + 1}")

if st.button('PDF表示'):
    st.title('PDF表示')
    invoice_show44()


# streamlit run pdf_oenshow01.py

# import streamlit as st
# import base64
#
# def main():
#     st.title("PDF Viewer")
#     pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])
#
#     if pdf_file is not None:
#         # PDFファイルをBase64エンコードしてHTMLタグに埋め込む
#         pdf_base64 = base64.b64encode(pdf_file.read()).decode("utf-8")
#         pdf_embed = f'<embed src="data:application/pdf;base64,{pdf_base64}" width="100%" height="600px" type="application/pdf">'
#         st.markdown(pdf_embed, unsafe_allow_html=True)
#
# if __name__ == "__main__":
#     main()
