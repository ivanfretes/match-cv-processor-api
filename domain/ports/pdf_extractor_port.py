"""Port (interface) for PDF extraction"""
from abc import ABC, abstractmethod
from typing import BinaryIO


class PDFExtractorPort(ABC):
    """Interface for PDF text extraction"""
    
    @abstractmethod
    async def extract_text(self, file_content: bytes, filename: str) -> tuple[str, int]:
        """
        Extract text from PDF file
        
        Args:
            file_content: PDF file content as bytes
            filename: Original filename
            
        Returns:
            Tuple of (extracted_text, total_pages)
            
        Raises:
            CVProcessingError: If extraction fails
        """
        pass

