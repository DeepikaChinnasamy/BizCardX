import streamlit as st
from conn import connect_db, insert_or_update_data

def show_alter():
    # Connect to the database
    conn = connect_db()
    cursor = conn.cursor()

    # Retrieve the last extracted data for editing
    cursor.execute("SELECT * FROM business_cards ORDER BY id DESC LIMIT 1")
    data = cursor.fetchone()

    if data:
        st.header("Alter Extracted Data")
        
        # Display the data with the ability to alter
        company_name = st.text_input("Company Name", value=data[1])
        card_holder_name = st.text_input("Card Holder Name", value=data[2])
        designation = st.text_input("Designation", value=data[3])
        mobile_number = st.text_input("Mobile Number", value=data[4])
        email_address = st.text_input("Email Address", value=data[5])
        website_url = st.text_input("Website URL", value=data[6])
        area = st.text_input("Area", value=data[7])
        city = st.text_input("City", value=data[8])
        state = st.text_input("State", value=data[9])
        pin_code = st.text_input("Pin Code", value=data[10])

        # Assuming you have the image stored as binary data
        image_data = data[11]

        # Create a dictionary with the altered data
        altered_data = {
            "company_name": company_name,
            "card_holder_name": card_holder_name,
            "designation": designation,
            "mobile_number": mobile_number,
            "email_address": email_address,
            "website_url": website_url,
            "area": area,
            "city": city,
            "state": state,
            "pin_code": pin_code,
        }

        # Save button
        if st.button("Save Changes"):
            status = insert_or_update_data(cursor, conn, altered_data, image_data)
            st.success(status)
    
    else:
        st.warning("No data found to alter.")

    # Close the database connection
    cursor.close()
    conn.close()
