import google.generativeai as genai
import os
import sys

# Add parent dir to path to allow importing config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

class AIService:
    """Handles interactions with the AI models for summarization."""
    
    def __init__(self):
        self.is_configured = False
        self._configure()
        
    def _configure(self):
        """Configure the Gemini API client."""
        from dotenv import load_dotenv
        import os
        
        # Explicitly define the path to .env file in the project root
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
        load_dotenv(dotenv_path=env_path, override=True)
        
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key and api_key != "your_gemini_api_key_here":
            genai.configure(api_key=api_key)
            self.is_configured = True
        
    def generate_summary(self, text, summary_type, tone, length):
        """
        Generate a summary using Gemini model based on user parameters.
        """
        if not self.is_configured:
            # Re-try configuration in case env vars were loaded late
            self._configure()
            if not self.is_configured:
                return False, "Gemini API key is not configured. Please add it to your .env file."
                
        try:
            # Use gemini-flash-latest for text tasks as 1.5 is deprecated
            model = genai.GenerativeModel('gemini-flash-latest')
            
            prompt = self._build_prompt(text, summary_type, tone, length)
            
            # Add safety settings to prevent blocking valid content unnecessarily
            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
            ]
            
            response = model.generate_content(
                prompt,
                safety_settings=safety_settings,
                generation_config={"temperature": 0.3} # Lower temp for more factual summaries
            )
            
            return True, response.text
            
        except Exception as e:
            return False, f"Error generating summary: {str(e)}"
            
    def _build_prompt(self, text, summary_type, tone, length):
        """Build a structured prompt based on the requested parameters."""
        
        # Length instructions
        length_instruction = {
            "Short": "Keep it very concise, roughly 1-2 paragraphs or 5-10 bullet points.",
            "Medium": "Provide a balanced summary, capturing main ideas and some supporting details.",
            "Long": "Provide a comprehensive and detailed summary, including all major points and key supporting evidence."
        }.get(length, "Keep it balanced.")
        
        # Type instructions
        type_instruction = {
            "Standard Summary": "Write a cohesive paragraph-based summary of the content.",
            "Bullet Points": "Extract the main points as a clear, organized list of bullet points.",
            "Key Insights": "Identify and list only the most critical insights, takeaways, or unique value propositions from the text.",
            "Action Items": "Extract any implied or explicit tasks, recommendations, or next steps from the text."
        }.get(summary_type, "Write a standard summary.")
        
        # Base prompt template
        prompt = f"""
You are an expert content analyzer and summarizer. Please process the following text according to these specifications:

FORMAT REQUIREMENTS:
- Type: {summary_type}. {type_instruction}
- Length: {length}. {length_instruction}
- Tone: {tone}.

TEXT TO SUMMARIZE:
------------------
{text}
------------------

Please provide the final output directly without any meta-commentary like "Here is the summary:" or "Based on the text:".
"""
        return prompt

# Singleton instance
ai_service = AIService()
