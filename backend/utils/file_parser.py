import os
import PyPDF2
import pdfplumber

def extract_text_from_file(file_obj, filename):
    """
    Extract text from uploaded files (PDF or TXT).
    
    Args:
        file_obj: Streamlit UploadedFile object
        filename (str): Name of the file to determine extension
        
    Returns:
        tuple: (success_bool, extracted_text_or_error_message)
    """
    try:
        file_ext = os.path.splitext(filename)[1].lower()
        
        if file_ext == '.txt':
            # Handle text files
            return True, file_obj.getvalue().decode("utf-8")
            
        elif file_ext == '.pdf':
            # Handle PDF files
            text = ""
            # Try with pdfplumber first as it's better for complex layouts
            try:
                with pdfplumber.open(file_obj) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                
                if text.strip():
                    return True, text
            except Exception:
                pass
                
            # Fallback to PyPDF2 if pdfplumber fails or returns empty
            if not text.strip():
                # Reset file pointer
                file_obj.seek(0)
                pdf_reader = PyPDF2.PdfReader(file_obj)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
            
            if not text.strip():
                return False, "Could not extract text from this PDF. It might be scanned or image-based."
                
            return True, text
            
        else:
            return False, f"Unsupported file type: {file_ext}. Please upload .txt or .pdf files."
            
    except UnicodeDecodeError:
        return False, "Error decoding file. Please ensure it's a valid text or PDF file."
    except Exception as e:
        return False, f"Error processing file: {str(e)}"

def count_words(text):
    """Return the word count of a given text."""
    if not text:
        return 0
    return len(text.split())
