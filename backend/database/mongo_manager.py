import pymongo
from pymongo.errors import ConnectionFailure
from datetime import datetime
import os
import sys

# Add parent dir to path to allow importing config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

class DatabaseManager:
    """Handles MongoDB connections and operations."""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        
    def connect(self):
        """Establish connection to MongoDB."""
        from dotenv import load_dotenv
        import os
        
        # Explicitly define the path to .env file in the project root
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
        load_dotenv(dotenv_path=env_path, override=True)
        
        mongo_uri = os.getenv("MONGODB_URI")
        
        if not mongo_uri:
            return False, "MongoDB URI not found in configuration."
            
        try:
            # We add a short timeout for quick failure if credentials are bad
            self.client = pymongo.MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            # Test connection
            self.client.admin.command('ping')
            
            db_name = os.getenv("MONGODB_DB_NAME", "ai_summarizer")
            self.db = self.client[db_name]
            self.collection = self.db["summaries"]
            return True, "Successfully connected to MongoDB."
        except ConnectionFailure as e:
            self.client = None
            return False, f"Failed to connect to MongoDB: {str(e)}"
        except Exception as e:
            self.client = None
            return False, f"Error initializing database: {str(e)}"
            
    def save_summary(self, original_text, summary_text, summary_type, tone, length, original_word_count, summary_word_count):
        """Save a generated summary to the database."""
        if not self.collection is not None:
            success, _ = self.connect()
            if not success:
                return False, "Database not connected."
                
        document = {
            "original_text_snippet": original_text[:500] + "..." if len(original_text) > 500 else original_text,
            "summary_text": summary_text,
            "summary_type": summary_type,
            "tone": tone,
            "length": length,
            "original_word_count": original_word_count,
            "summary_word_count": summary_word_count,
            "compression_ratio": round((summary_word_count / original_word_count) * 100, 2) if original_word_count > 0 else 0,
            "timestamp": datetime.now()
        }
        
        try:
            result = self.collection.insert_one(document)
            return True, str(result.inserted_id)
        except Exception as e:
            return False, f"Failed to save summary: {str(e)}"
            
    def get_recent_summaries(self, limit=10):
        """Retrieve recent summaries from the database."""
        if not self.collection is not None:
            success, _ = self.connect()
            if not success:
                return []
                
        try:
            cursor = self.collection.find().sort("timestamp", pymongo.DESCENDING).limit(limit)
            return list(cursor)
        except Exception:
            return []

# Singleton instance
db_manager = DatabaseManager()
