import streamlit as st
from PIL import Image
import pytesseract
import json

# Configure Tesseract path (if needed)
pytesseract.pytesseract.tesseract_cmd = r'./Tesseract-OCR/tesseract.exe'

def extract_text(image):
    """Extract text from an image using Tesseract OCR."""
    text = pytesseract.image_to_string(image, lang='eng+hin')
    return text

def search_keywords(text, keyword):
    """Search for keywords in the extracted text."""
    if keyword.lower() in text.lower():
        return True, text.lower().index(keyword.lower())
    return False, -1

def main():
    st.title("OCR and Document Search Web Application")
    
    # Image upload
    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        
        # Extract text
        extracted_text = extract_text(image)
        st.subheader("Extracted Text")
        st.write(extracted_text)
        
        # Search functionality
        keyword = st.text_input("Enter Keyword to Search:")
        if st.button("Search"):
            found, index = search_keywords(extracted_text, keyword)
            if found:
                st.success(f"Keyword '{keyword}' found at index {index}!")
            else:
                st.error(f"Keyword '{keyword}' not found in the extracted text.")

if __name__ == "__main__":
    main()
