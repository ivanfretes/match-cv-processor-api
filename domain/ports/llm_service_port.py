"""Port (interface) for LLM services"""
from abc import ABC, abstractmethod


class LLMServicePort(ABC):
    """Interface for LLM services (OpenAI, etc.)"""
    
    @abstractmethod
    async def generate_cv_summary(
        self,
        cv_text: str,
        language: str = "spanish"
    ) -> str:
        """
        Generate a CV summary using LLM
        
        Args:
            cv_text: Text content of the CV
            language: Language for the summary (spanish/english)
            
        Returns:
            Generated summary text
            
        Raises:
            Exception: If summary generation fails
        """
        pass

