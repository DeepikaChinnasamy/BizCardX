import streamlit as st
import cv2
from Ext_EC_ocr import extract_text_from_image

def show_upload():
    st.title("Upload Business Card Image")
    uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = uploaded_file.read()
        original_image_path = 'temp_image.png'
        with open(original_image_path, 'wb') as f:
            f.write(image)

        extracted_texts = extract_text_from_image(original_image_path)
        st.session_state['extracted_texts'] = extracted_texts  # Save extracted texts for later use

        # Display images side by side
        col1, col2 = st.columns(2)

        with col1:
            st.image(image, caption='Original Image', use_column_width=True)
        
        with col2:
            annotated_image = cv2.imread('temp_image_with_annotations.png')
            if annotated_image is not None:
                st.image(cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB), caption='OCR Processed Image', use_column_width=True)

                