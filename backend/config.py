import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration variables."""
    
    @property
    def APP_NAME(self):
        return os.getenv("APP_NAME", "AI-Powered Content Summarizer")
    
    # API Keys
    @property
    def GEMINI_API_KEY(self):
        return os.getenv("GEMINI_API_KEY")
        
    @property
    def OPENAI_API_KEY(self):
        return os.getenv("OPENAI_API_KEY")
    
    # Database
    @property
    def MONGODB_URI(self):
        return os.getenv("MONGODB_URI")
        
    @property
    def MONGODB_DB_NAME(self):
        return os.getenv("MONGODB_DB_NAME", "ai_summarizer")
    
    # File handling
    UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")
    ALLOWED_EXTENSIONS = {".pdf", ".txt"}

    
    @classmethod
    def ensure_directories(cls):
        """Ensure necessary directories exist."""
        if not os.path.exists(cls.UPLOAD_DIR):
            os.makedirs(cls.UPLOAD_DIR)
