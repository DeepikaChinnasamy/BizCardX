import streamlit as st
import pandas as pd
from conn import connect_db, create_table, insert_or_update_data
from Ext_EC_ocr import validate_and_extract_info

def show_extraction():
    st.title("Extracted Information")
    
    if 'extracted_texts' in st.session_state:
        validated_data = validate_and_extract_info(st.session_state['extracted_texts'])
        st.write("Extracted Information:")
        if validated_data:
            df = pd.DataFrame([validated_data])
            st.dataframe(df)
            st.session_state['validated_data'] = validated_data  # Save for later use

            if st.button("Save to Database"):
                conn = connect_db()
                c = conn.cursor()
                create_table(c, conn)
                with open('temp_image.png', 'rb') as image_file:
                    image_data = image_file.read()
                status = insert_or_update_data(c, conn, validated_data, image_data)
                st.success(status)
                c.close()
                conn.close()
    else:
        st.warning("No data available. Please upload an image first.")
