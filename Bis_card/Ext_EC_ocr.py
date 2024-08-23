import re
import warnings
import easyocr
import cv2
import matplotlib.pyplot as plt

def extract_text_from_image(image_path):
    """
    Extracts text from an image using easyOCR, draws bounding boxes around detected text,
    and returns the extracted text.
    
    Args:
        image_path (str): The path to the image file.
    
    Returns:
        list of str: Extracted text from the image.
    """
    # Suppress warnings
    warnings.filterwarnings("ignore", category=FutureWarning)

    # Load the image
    original_image = cv2.imread(image_path)

    if original_image is None:
        print(f"Failed to load the image. Check the file path: {image_path}")
        return []

    # Make a copy of the original image for annotations
    annotated_image = original_image.copy()

    # Initialize the easyOCR reader
    reader = easyocr.Reader(['en'])

    # Perform OCR on the image
    results = reader.readtext(original_image)

    # Draw bounding boxes and collect text
    extracted_texts = []
    for (bbox, text, prob) in results:
        extracted_texts.append(text)
        # Draw bounding box and text on the image
        top_left = tuple([int(val) for val in bbox[0]])
        bottom_right = tuple([int(val) for val in bbox[2]])
        annotated_image = cv2.rectangle(annotated_image, top_left, bottom_right, (0, 255, 0), 2)
        annotated_image = cv2.putText(annotated_image, text, top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

    # Save the output image with annotations
    annotated_image_path = 'temp_image_with_annotations.png'
    cv2.imwrite(annotated_image_path, annotated_image)

    # Show the output image with annotations
    plt.imshow(cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

    print(extracted_texts)
    return extracted_texts

def validate_and_extract_info(extracted_texts):
    """
    Validates and extracts specific fields from the OCR extracted texts.
    
    Args:
        extracted_texts (list of str): List of texts extracted from the image.
    
    Returns:
        dict: Dictionary containing validated and extracted fields.
    """
    data = {
        "company_name": "",
        "card_holder_name": "",
        "designation": "",
        "mobile_number": "",
        "email_address": "",
        "website_url": "",
        "area": "",
        "city": "",
        "state": "",
        "pin_code": "",
    }
    
    # Regex patterns
    phone_number_pattern = re.compile(r'^\+?\d{1,4}[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$')
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    website_pattern = re.compile(r'\b(https?://)?(www\.)?\w+\.\w+\b')
    pincode_pattern = re.compile(r'^\d{6,}$')
    state_pattern = re.compile(r'\b[Tt]amil[Nn]adu\b|\b[Kk]arnataka\b|\b[Mm]aharashtra\b|\b[Pp]unjab\b|\b[Kk]erala\b')  # Add more states as needed


    for ind, text in enumerate(extracted_texts):
        
        text_lower = text.lower().strip()

        # Get COMPANY NAME (concatenate the last and second-to-last elements)
        if ind == len(extracted_texts) - 2:
            if not (email_pattern.search(text) or website_pattern.search(text) or phone_number_pattern.match(text)
                    or pincode_pattern.match(text) or state_pattern.search(text)):
                data["company_name"] = text  # Start with the second-to-last element
        elif ind == len(extracted_texts) - 1:
            data["company_name"] = data["company_name"] + " " + text  # Append the last element


        
        # Get CARD HOLDER NAME (first element)
        elif ind == 0:
            data["card_holder_name"] = text
        
        # Get DESIGNATION (second element)
        elif ind == 1:
            data["designation"] = text
        
        # Get AREA (patterns matching area-like formats)
        if re.search(r'^[0-9].+, [a-zA-Z]+', text):
            data["area"] = text.split(',')[0]
        elif re.search(r'[0-9] [a-zA-Z]+', text):
            data["area"] = text
        
        # Get CITY NAME (common patterns for city names)
        match1 = re.findall(r'.*St , ([a-zA-Z]+).*', text)
        match2 = re.findall(r'.*St,, ([a-zA-Z]+).*', text)
        match3 = re.findall(r'^[E].*', text)
        if match1:
            data["city"] = match1[0]
        elif match2:
            data["city"] = match2[0]
        elif match3:
            data["city"] = match3[0]
        
        # Get STATE (patterns matching state-like formats)
        state_match = re.findall(r'[a-zA-Z]{9} +[0-9]', text)
        if state_match:
            data["state"] = text[:9]
        elif re.search(r'[0-9].+, ([a-zA-Z]+);', text):
            data["state"] = text.split()[-1]
        
        # Get PINCODE (6+ digit numbers)
        if len(text) >= 6 and text.isdigit():
            data["pin_code"] = text
        elif re.search(r'[a-zA-Z]{9} +[0-9]', text):
            data["pin_code"] = text[10:]
        
        # Validate EMAIL and WEBSITE
        if email_pattern.search(text):
            data["email_address"] = text
        elif website_pattern.search(text):
            data["website_url"] = text
        elif phone_number_pattern.match(text):
            data["mobile_number"] = text

    return data
