import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.database.mongo_manager import db_manager

def show_dashboard():
    st.header("📊 Usage Dashboard & History")
    st.markdown("View your recent summaries and usage statistics.")
    
    # Check DB connection
    success, msg = db_manager.connect()
    if not success:
        st.error(f"Database connection error: {msg}")
        st.info("Please ensure MongoDB URI is set in your .env file.")
        return
        
    recent_summaries = db_manager.get_recent_summaries(limit=20)
    
    if not recent_summaries:
        st.info("No summaries found in the database yet. Generate some summaries to see them here!")
        return
        
    # Metrics row
    col1, col2, col3 = st.columns(3)
    
    total_processed = len(recent_summaries)
    total_words_original = sum(item.get("original_word_count", 0) for item in recent_summaries)
    total_words_summary = sum(item.get("summary_word_count", 0) for item in recent_summaries)
    
    avg_compression = 0
    if total_words_original > 0:
        avg_compression = round((total_words_summary / total_words_original) * 100, 1)
    
    with col1:
        st.metric("Total Documents Processed", total_processed)
    with col2:
        st.metric("Words Summarized", f"{total_words_original:,}")
    with col3:
        st.metric("Avg. Compression Ratio", f"{avg_compression}%")
        
    st.divider()
    
    # History Table
    st.subheader("Recent History")
    
    # Format data for dataframe
    df_data = []
    for item in recent_summaries:
        df_data.append({
            "Date": item.get("timestamp").strftime("%Y-%m-%d %H:%M") if item.get("timestamp") else "Unknown",
            "Type": item.get("summary_type", "N/A"),
            "Length": item.get("length", "N/A"),
            "Original Words": item.get("original_word_count", 0),
            "Summary Words": item.get("summary_word_count", 0),
            "ID": str(item.get("_id"))
        })
        
    df = pd.DataFrame(df_data)
    
    # Display table without the ID column
    display_df = df.drop(columns=["ID"])
    st.dataframe(display_df, use_container_width=True)
    
    # Option to view specific summary details
    st.subheader("View Past Summary")
    
    selected_idx = st.selectbox(
        "Select a recent summary to view details:",
        range(len(recent_summaries)),
        format_func=lambda i: f"{df_data[i]['Date']} - {df_data[i]['Type']} ({df_data[i]['Original Words']} words)"
    )
    
    if selected_idx is not None:
        selected_item = recent_summaries[selected_idx]
        
        with st.expander("Show Details", expanded=True):
            st.markdown("### Generated Summary")
            st.write(selected_item.get("summary_text", ""))
            
            st.divider()
            
            st.markdown("### Original Text Snippet")
            st.text(selected_item.get("original_text_snippet", ""))
            
            # Download button for past summary
            st.download_button(
                label="📥 Download This Summary",
                data=selected_item.get("summary_text", ""),
                file_name=f"summary_{selected_item.get('timestamp').strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
