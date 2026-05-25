import streamlit as st
import sys
import os

# Ensure absolute imports work from the root of the project
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend.components.ui_helpers import set_page_config, apply_custom_css, render_header, render_sidebar
from backend.utils.file_parser import extract_text_from_file, count_words
from backend.services.ai_service import ai_service
from backend.database.mongo_manager import db_manager
from frontend.components.dashboard_view import show_dashboard

def main():
    # Set standard UI configuration
    set_page_config()
    apply_custom_css()
    
    # Main Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Summarizer", "Dashboard"])
    
    if page == "Summarizer":
        render_summarizer_page()
    else:
        show_dashboard()

def render_summarizer_page():
    render_header()
    
    # Get user settings from sidebar
    settings = render_sidebar()
    
    # Main content area tabs
    tab1, tab2 = st.tabs(["📝 Text Input", "📄 File Upload"])
    
    input_text = ""
    source_type = None
    
    with tab1:
        st.markdown("### Enter text to summarize")
        text_area = st.text_area("Paste your content here:", height=300, placeholder="Paste articles, reports, or any long-form text here...")
        if text_area:
            input_text = text_area
            source_type = "text_input"
            
    with tab2:
        st.markdown("### Upload a document")
        uploaded_file = st.file_uploader("Choose a PDF or TXT file", type=['pdf', 'txt'])
        
        if uploaded_file is not None:
            with st.spinner("Extracting text from file..."):
                success, result = extract_text_from_file(uploaded_file, uploaded_file.name)
                
                if success:
                    st.success(f"Successfully extracted {count_words(result)} words from {uploaded_file.name}")
                    with st.expander("Preview Extracted Text"):
                        st.text(result[:1000] + "..." if len(result) > 1000 else result)
                    input_text = result
                    source_type = "file_upload"
                else:
                    st.error(result)
    
    # Processing section
    st.divider()
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        generate_btn = st.button("Generate Summary 🚀", use_container_width=True)
        
    if generate_btn:
        if not input_text or len(input_text.strip()) < 10:
            st.warning("Please provide more text to summarize (minimum 10 characters).")
            return
            
        process_summary(input_text, settings)

def process_summary(input_text, settings):
    """Handle the flow of generating, displaying, and saving a summary."""
    original_word_count = count_words(input_text)
    
    # Show processing state
    progress_text = "Analyzing content and generating summary..."
    my_bar = st.progress(0, text=progress_text)
    
    # Call AI Service
    my_bar.progress(30, text="Sending to AI Engine...")
    success, result = ai_service.generate_summary(
        text=input_text,
        summary_type=settings["type"],
        tone=settings["tone"],
        length=settings["length"]
    )
    
    my_bar.progress(80, text="Finalizing output...")
    
    if success:
        my_bar.progress(100, text="Complete!")
        summary_word_count = count_words(result)
        
        # Display Results
        st.markdown("## 📋 Your Summary")
        
        # Stats row
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        with stat_col1:
            st.metric("Original Word Count", original_word_count)
        with stat_col2:
            st.metric("Summary Word Count", summary_word_count)
        with stat_col3:
            reduction = round((1 - (summary_word_count / original_word_count)) * 100) if original_word_count > 0 else 0
            st.metric("Content Reduced By", f"{reduction}%")
            
        # Summary Card
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.write(result)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Actions
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Download as TXT",
                data=result,
                file_name=f"summary_{settings['type'].replace(' ', '_').lower()}.txt",
                mime="text/plain",
                use_container_width=True
            )
            
        # Save to database in background
        with st.spinner("Saving to database..."):
            db_success, db_msg = db_manager.save_summary(
                original_text=input_text,
                summary_text=result,
                summary_type=settings["type"],
                tone=settings["tone"],
                length=settings["length"],
                original_word_count=original_word_count,
                summary_word_count=summary_word_count
            )
            
            if not db_success:
                st.toast(f"Note: Could not save to history. {db_msg}")
            
    else:
        my_bar.empty()
        st.error(f"Failed to generate summary: {result}")
        if "API key" in result:
            st.info("💡 Please make sure you have added your Gemini API key to the .env file.")

if __name__ == "__main__":
    main()
