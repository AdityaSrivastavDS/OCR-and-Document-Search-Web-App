# OCR and Document Search Web Application

## Deployed Link:
https://ocr-document-search.streamlit.app/

## Overview
This is a web application that performs Optical Character Recognition (OCR) on uploaded images containing text in both Hindi and English. The application allows users to upload an image, extract text from it, and search for keywords within the extracted text.

## Features
- Upload images in JPEG or PNG format.
- Extract text using Tesseract or EasyOCR.
- Search for keywords within the extracted text.
- User-friendly interface using Streamlit.

## Requirements
- Python 3.6+
- Tesseract-OCR (if using Tesseract) or EasyOCR
- Required Python libraries listed in `requirements.txt`

## Setup Instructions

1. **Clone the Repository**
Clone this repository to your local machine:
```bash
git clone https://github.com/AdityaSrivastavDS/OCR-and-Document-Search-Web-App
cd OCR-and-Document-Search-Web-App
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the Application**
To run the application locally, use the following command:
```bash
streamlit run app.py
```

## Usage Instructions
- Open the deployed application URL.
- Upload an image file that contains text in Hindi or English.
- View the extracted text.
- Enter keywords to search within the extracted text and click "Search" to see results