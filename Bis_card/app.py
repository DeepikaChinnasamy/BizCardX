import streamlit as st
from app_pages.home import show_home
from app_pages.upload import show_upload
from app_pages.extraction import show_extraction
from app_pages.alter import show_alter


def main():
    st.set_page_config(page_title="BizCardX: Extracting Business Card Data with OCR | By Deepika",
                       layout="wide",
                       initial_sidebar_state="expanded",
                       menu_items={'About': """# This OCR app is created by *Deepika*!"""})
    
    # Set the background image
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://wallpapers.com/images/hd/geometric-gradient-color-c4j64ru3pangd4in.webp");
            background-size: cover;
            background-position: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Sidebar Navigation
    # st.sidebar.title("Navigation")
    options = ["Home", "Upload", "Extraction", "Alter"]
    choice = st.sidebar.radio("Business Card", options)

    if choice == "Home":
        show_home()
    elif choice == "Upload":
        show_upload()
    elif choice == "Extraction":
        show_extraction()
    elif choice == "Alter":
        show_alter()


if __name__ == "__main__":
    main()
