# AI-Powered Content Summarizer

A full-stack AI-powered web application that generates structured, customizable summaries from long-form text or documents (PDF, TXT) using advanced Generative AI models.

## Features

- **Document Processing**: Extract text from uploaded PDF and TXT files.
- **Direct Text Input**: Paste long-form content directly for immediate summarization.
- **Customizable AI**: 
  - 4 Summary Types (Standard, Bullet Points, Key Insights, Action Items)
  - 3 Length settings (Short, Medium, Long)
  - 4 Tones (Professional, Casual, Academic, Executive)
- **History & Dashboard**: View, analyze, and download past summaries stored in MongoDB.
- **Modern UI**: Clean, professional, and responsive Streamlit interface.

## Tech Stack

- **Frontend**: Streamlit (Python)
- **Backend**: Python
- **Database**: MongoDB (PyMongo)
- **AI Integration**: Google Gemini API (`google-generativeai`)
- **Document Parsing**: `pdfplumber`, `PyPDF2`

## Project Structure

```
AI-Content-Summarizer/
│
├── frontend/                 # UI components and pages
│   ├── app.py                # Main Streamlit application
│   ├── pages/
│   │   └── dashboard.py      # Usage history and statistics
│   └── components/
│       └── ui_helpers.py     # Custom CSS and UI render functions
│
├── backend/                  # Core application logic
│   ├── config.py             # Environment configuration
│   ├── services/
│   │   └── ai_service.py     # AI model integration
│   ├── database/
│   │   └── mongo_manager.py  # MongoDB operations
│   └── utils/
│       └── file_parser.py    # PDF/TXT extraction utilities
│
├── uploads/                  # Temporary file storage (auto-created)
├── .env                      # Environment variables (create from .env.example)
└── requirements.txt          # Project dependencies
```

## Setup & Installation

1. **Clone the repository** (if applicable) or navigate to the project directory.

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and add your specific API keys and Database URI:
     - Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/)
     - Get a MongoDB URI from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

## Running the Application

Start the Streamlit server by running the main app file from the project root:

```bash
streamlit run frontend/app.py
```

The application will typically be available at `http://localhost:8501`.
