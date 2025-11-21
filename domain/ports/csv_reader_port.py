"""Port (interface) for CSV reading"""
from abc import ABC, abstractmethod
from typing import List, Dict


class CSVReaderPort(ABC):
    """Interface for CSV file reading"""
    
    @abstractmethod
    async def read_csv(self, file_content: bytes, filename: str) -> tuple[List[str], List[Dict[str, str]]]:
        """
        Read CSV file content
        
        Args:
            file_content: CSV file content as bytes
            filename: Original filename
            
        Returns:
            Tuple of (columns, rows) where rows is a list of dictionaries
            
        Raises:
            CSVProcessingError: If reading fails
        """
        pass

