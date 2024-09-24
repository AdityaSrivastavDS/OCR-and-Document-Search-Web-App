import streamlit as st
from PIL import Image
import easyocr
import hashlib

# Cache the OCR model to avoid reloading it
@st.cache_resource(ttl=3600, max_entries=2)
def load_ocr_model(gpu=False):
    """
    Load the EasyOCR model (English and Hindi).
    Use GPU if available, else fall back to CPU.
    """
    try:
        # Initialize EasyOCR Reader with GPU support if available
        reader = easyocr.Reader(['en', 'hi'], gpu=gpu)
        return reader
    except Exception as e:
        st.error("Error loading OCR model. Please try again later.")
        return None

# Let user decide whether to use GPU (if available)
use_gpu = st.sidebar.checkbox("Use GPU (if available)", value=False)
reader = load_ocr_model(gpu=use_gpu)

# Function to create a unique hash for the image
def get_image_hash(image):
    """Generate a hash for the image based on its content."""
    return hashlib.md5(image.tobytes()).hexdigest()

# Caching the extracted text using Streamlit's caching mechanism
@st.cache_data(ttl=3600, max_entries=10)
def extract_text(image):
    """Extract text from an image using EasyOCR and cache the result."""
    try:
        # Perform OCR if reader is available
        if reader is not None:
            results = reader.readtext(image)
            text = ' '.join([result[1] for result in results])
            return text
        else:
            return "OCR model not loaded."
    except Exception as e:
        return "Error extracting text. Please try with a different image."

def search_keywords(text, keyword):
    """Search for keywords in the extracted text."""
    if keyword.lower() in text.lower():
        return True, text.lower().index(keyword.lower())
    return False, -1

def main():
    st.title("OCR and Document Search Web Application")
    st.write("Extract text from images and search for keywords in the extracted text.")

    # Image upload
    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_column_width=True)
            
            # Extract text from the image
            with st.spinner("Extracting text..."):
                extracted_text = extract_text(image)
            st.subheader("Extracted Text")
            st.write(extracted_text)

            # Search functionality
            keyword = st.text_input("Enter Keyword to Search:")
            if st.button("Search"):
                if extracted_text:
                    found, index = search_keywords(extracted_text, keyword)
                    if found:
                        st.success(f"Keyword '{keyword}' found at index {index}!")
                    else:
                        st.error(f"Keyword '{keyword}' not found in the extracted text.")
                else:
                    st.error("No text to search. Please upload a valid image.")

        except Exception as e:
            st.error("Error processing the image. Please upload a valid image file.")

if __name__ == "__main__":
    main()
