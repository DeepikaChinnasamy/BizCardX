import streamlit as st

def show_home():
    st.title("Welcome to BizCardX - Business Card Information Extractor")
    # st.title("BizCardX: Extracting Business Card Data with OCR")
    # st.write("Upload a business card image to extract and validate the information.")
    st.write("""
    Extracting Business Card Data with OCR Overview BizCardX is a Streamlit web application which extracts data from business cards using Optical Character Recognition (OCR). Users can upload an image of a business card and the application uses the easyOCR library to extract relevant information from the card. The extracted information is then displayed in a user-friendly format and can be stored in a MySQL database for future reference.

    The application allows users to view, modify, or delete the extracted data. It also has a user interface for uploading business card images and a table interface for displaying the extracted data. The application is created by Deepika. C.

    Prerequisites To run this application, you'll need:

    ==> Python environment (Python 3.x recommended)
             
    ==> Streamlit,
              
    ==> Pandas,
             
    ==> easyOCR,
             
    ==> PIL,
             
    ==> cv2,
             
    ==> matplotlib,
             
    ==> re,
             
    ==> Postgresql
    """)
