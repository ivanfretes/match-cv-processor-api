"""Use case for processing CSV files"""
from domain.entities.csv_document import CSVDocument
from domain.ports.csv_reader_port import CSVReaderPort
from domain.exceptions.domain_exceptions import CSVProcessingError


class ProcessCSVUseCase:
    """Use case for processing CSV files"""
    
    def __init__(self, csv_reader: CSVReaderPort):
        """
        Initialize the use case
        
        Args:
            csv_reader: Service for reading CSV files
        """
        self.csv_reader = csv_reader
    
    async def execute(self, file_content: bytes, filename: str) -> CSVDocument:
        """
        Execute the CSV processing use case
        
        Args:
            file_content: CSV file content as bytes
            filename: Original filename
            
        Returns:
            CSVDocument entity with processed data
            
        Raises:
            CSVProcessingError: If processing fails
        """
        try:
            # Read CSV content
            columns, rows = await self.csv_reader.read_csv(file_content, filename)
            
            # Create CSV document entity
            csv_document = CSVDocument(
                filename=filename,
                total_rows=len(rows),
                columns=columns,
                data=rows
            )
            
            return csv_document
            
        except Exception as e:
            raise CSVProcessingError(f"Error al procesar el CSV: {str(e)}") from e

