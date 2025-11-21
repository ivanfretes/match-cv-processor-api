"""Port (interface) for text cleaning"""
from abc import ABC, abstractmethod


class TextCleanerPort(ABC):
    """Interface for text cleaning and normalization"""
    
    @abstractmethod
    def clean(self, text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned and normalized text
        """
        pass

