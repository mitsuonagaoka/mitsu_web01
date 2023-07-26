import streamlit as st
import pdfplumber
from io import BytesIO
from PIL import Image

def pdf_to_image(pdf_file):
    images = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            img = page.to_image(resolution=150)
            images.append(img)

    return images

def main():
    st.title("PDF Viewer")
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if pdf_file is not None:
        images = pdf_to_image(pdf_file)
        for img in images:
            st.image(img)

if __name__ == "__main__":
    main()


# invoice_show44()

# streamlit run pdf_show04.py
