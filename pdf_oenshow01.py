# import sqlite3
# import pandas as pd
# import streamlit as st
# from PIL import Image
# import datetime
# from datetime import date

# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import portrait, A4
# from reportlab.lib.utils import ImageReader
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.cidfonts import UnicodeCIDFont
# from contextlib import closing
# import plotly.express as px
# import base64
# import qrcode

import streamlit as st
from pdf2image import convert_from_path
from reportlab.pdfbase.ttfonts import TTFont
import pytesseract
import os

# streamlit run pdf_oenshow01.py

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
