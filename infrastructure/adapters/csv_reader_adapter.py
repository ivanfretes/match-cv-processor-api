"""CSV reader adapter - Implements CSVReaderPort"""
import csv
import io
from typing import List, Dict
from domain.ports.csv_reader_port import CSVReaderPort
from domain.exceptions.domain_exceptions import CSVProcessingError


class CSVReaderAdapter(CSVReaderPort):
    """Adapter for CSV reading using Python's csv module"""
    
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
        try:
            # Decode the content
            content_str = file_content.decode('utf-8')
            
            # Read the CSV
            csv_reader = csv.DictReader(io.StringIO(content_str))
            rows = list(csv_reader)
            
            # Get column names
            if rows:
                columns = list(rows[0].keys())
            else:
                columns = []
            
            return columns, rows
            
        except UnicodeDecodeError as e:
            raise CSVProcessingError("Error de codificación. El archivo debe estar en UTF-8") from e
        except Exception as e:
            raise CSVProcessingError(f"Error al procesar el CSV: {str(e)}") from e

