import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import re

# Cache the OCR model to avoid reloading it
@st.cache_resource(ttl=3600, max_entries=2)
def load_ocr_model(gpu=False):
    # Initialize the EasyOCR model for English and Hindi, with GPU handling
    reader = easyocr.Reader(['en', 'hi'], gpu=gpu)
    return reader

# Load OCR model (toggle gpu=False if not using a GPU)
reader = load_ocr_model(gpu=False)

# Function to extract text from the image using EasyOCR
def extract_text(image):
    """Extract text from an image using EasyOCR."""
    # Convert the PIL image to a NumPy array
    image_np = np.array(image)
    
    # Perform OCR
    results = reader.readtext(image_np)
    
    # Extract text from OCR results
    text = ' '.join([result[1] for result in results])
    
    return text

# Function to normalize and clean the extracted text
def clean_text(text):
    """Normalize text by removing extra spaces and converting it to a consistent format."""
    # Remove extra spaces and line breaks
    text = ' '.join(text.split())
    
    # Optional: You can also normalize Unicode characters here
    return text

# Function to search for keywords in the extracted text
def search_keywords(text, keyword):
    """Search for keywords in the extracted text."""
    # Normalize both the extracted text and the keyword for better matching
    text_clean = clean_text(text)
    keyword_clean = clean_text(keyword)
    
    # Use regex for case-insensitive search
    match = re.search(re.escape(keyword_clean), text_clean, re.IGNORECASE)
    
    if match:
        return True, match.start()
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
