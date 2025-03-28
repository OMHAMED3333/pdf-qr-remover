import streamlit as st
import fitz  # PyMuPDF
import io
import os
from PIL import Image
import time

def remove_qr_codes(input_pdf_bytes, progress_bar):
    """
    Process PDF to remove QR codes
    """
    # Open the PDF from bytes
    doc = fitz.open(stream=input_pdf_bytes, filetype="pdf")
    total_pages = len(doc)
    
    for page_num in range(total_pages):
        page = doc[page_num]
        images = page.get_images(full=True)
        
        # Update progress
        progress = (page_num + 1) / total_pages
        progress_bar.progress(progress)
        
        # Remove each image (this is a simple approach - you might want more sophisticated QR detection)
        for img in images:
            page.delete_image(img[0])
    
    # Save to bytes buffer
    output_buffer = io.BytesIO()
    doc.save(output_buffer)
    doc.close()
    output_buffer.seek(0)
    
    return output_buffer

def main():
    st.title("PDF QR Code Remover")
    st.write("Upload a PDF file to remove QR codes from it")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Display file info
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size / 1024:.2f} KB"
        }
        st.write(file_details)
        
        # Process button
        if st.button("Remove QR Codes"):
            # Create progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("Processing PDF...")
            
            # Read the uploaded file into bytes
            input_pdf_bytes = uploaded_file.read()
            
            # Process the PDF
            start_time = time.time()
            cleaned_pdf = remove_qr_codes(input_pdf_bytes, progress_bar)
            processing_time = time.time() - start_time
            
            status_text.text(f"Processing completed in {processing_time:.2f} seconds!")
            
            # Download button
            st.download_button(
                label="Download Cleaned PDF",
                data=cleaned_pdf,
                file_name=f"cleaned_{uploaded_file.name}",
                mime="application/pdf"
            )

if __name__ == "__main__":
    main()