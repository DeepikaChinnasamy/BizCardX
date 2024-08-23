from conn import connect_db, create_table, insert_or_update_data
from Ext_EC_ocr import extract_text_from_image, validate_and_extract_info



def process_business_card(image_path):
    """
    Processes a business card image to extract and validate information.
    
    Args:
        image_path (str): The path to the image file.
    
    Returns:
        dict: Dictionary containing validated and extracted fields.
    """
    extracted_texts = extract_text_from_image(image_path)
    if not extracted_texts:
        return {}
    
    validated_data = validate_and_extract_info(extracted_texts)
    
    # Connect to the database and create the table
    conn = connect_db()
    c = conn.cursor()
    create_table(c, conn)
    
    # Optionally, you might want to save the image as binary for insertion
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    
    # Insert or update data and get the status
    status = insert_or_update_data(c, conn, validated_data, image_data)
    
    print(status)  # Print the status message
    
    c.close()
    conn.close()
    
    return validated_data

# Example usage
# image_path = r'C:/Deepika/Project_own/Guvi/Bizcardx/Biz/images/1.png'
# validated_data = process_business_card(image_path)
# print(validated_data)
