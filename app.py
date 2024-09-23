import streamlit as st
from PIL import Image
import easyocr


# Cache the OCR model to avoid reloading it
@st.cache_resource
def load_ocr_model():
    # Initialize the EasyOCR model for English and Hindi
    reader = easyocr.Reader(['en', 'hi'])
    return reader

# Use the cached model
reader = load_ocr_model()

def extract_text(image):
    """Extract text from an image using EasyOCR."""
    results = reader.readtext(image)
    text = ' '.join([result[1] for result in results])
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
