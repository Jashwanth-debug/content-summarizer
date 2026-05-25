import streamlit as st

def set_page_config():
    """Configure standard page settings for the Streamlit app."""
    st.set_page_config(
        page_title="AI Summarizer Pro",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def apply_custom_css():
    """Apply custom CSS to modernize the Streamlit UI."""
    st.markdown("""
        <style>
        /* Main theme adjustments */
        .main {
            background-color: #f8f9fa;
        }
        
        /* Typography adjustments */
        h1, h2, h3 {
            color: #1E3A8A;
            font-family: 'Inter', sans-serif;
            font-weight: 700;
        }
        
        /* Modern Card Styling */
        .stCard {
            background-color: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            margin-bottom: 24px;
            border: 1px solid #e5e7eb;
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        }
        
        .stCard:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }
        
        /* Button styling */
        .stButton > button {
            background-color: #2563EB;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.2s;
        }
        
        .stButton > button:hover {
            background-color: #1D4ED8;
            box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3);
            border: none;
            color: white;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #ffffff;
            border-right: 1px solid #e5e7eb;
        }
        
        /* Input fields */
        .stTextArea > div > div > textarea {
            border-radius: 8px;
            border: 1px solid #d1d5db;
        }
        
        .stTextArea > div > div > textarea:focus {
            border-color: #2563EB;
            box-shadow: 0 0 0 1px #2563EB;
        }
        
        /* Metric styling */
        [data-testid="stMetricValue"] {
            color: #2563EB;
            font-weight: 700;
        }
        
        /* Upload box */
        [data-testid="stFileUploadDropzone"] {
            border: 2px dashed #93C5FD;
            border-radius: 12px;
            background-color: #EFF6FF;
        }
        
        [data-testid="stFileUploadDropzone"]:hover {
            border-color: #2563EB;
            background-color: #DBEAFE;
        }
        </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render the application header with title and subtitle."""
    col1, col2 = st.columns([1, 5])
    with col1:
        st.markdown("<h1 style='text-align: center; font-size: 3rem;'>🧠</h1>", unsafe_allow_html=True)
    with col2:
        st.title("AI Content Summarizer")
        st.markdown("<p style='font-size: 1.2rem; color: #4B5563; margin-top: -15px;'>Transform lengthy documents and text into actionable insights instantly.</p>", unsafe_allow_html=True)
    st.divider()

def render_sidebar():
    """Render the sidebar configuration options and return selected settings."""
    with st.sidebar:
        st.header("⚙️ Settings")
        
        st.subheader("Summary Configuration")
        summary_type = st.selectbox(
            "Format",
            ["Standard Summary", "Bullet Points", "Key Insights", "Action Items"],
            help="Choose the structural format of your summary"
        )
        
        length = st.select_slider(
            "Length",
            options=["Short", "Medium", "Long"],
            value="Medium",
            help="Select how detailed you want the summary to be"
        )
        
        tone = st.selectbox(
            "Tone",
            ["Professional", "Casual", "Academic", "Executive"],
            help="Select the tone of voice for the generated text"
        )
        
        st.divider()
        
        st.subheader("About")
        st.info("This AI-powered application extracts text from your documents and uses advanced Language Models to generate precise, structured summaries based on your preferences.")
        
        return {
            "type": summary_type,
            "length": length,
            "tone": tone
        }
