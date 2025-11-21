"""PyPDF adapter - Implements PDFExtractorPort using pypdf"""
import io
from pypdf import PdfReader
from domain.ports.pdf_extractor_port import PDFExtractorPort
from domain.exceptions.domain_exceptions import CVProcessingError


class PyPDFExtractor(PDFExtractorPort):
    """Adapter for PDF extraction using pypdf library"""
    
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
        try:
            # Create PdfReader from bytes
            pdf_file = io.BytesIO(file_content)
            reader = PdfReader(pdf_file)
            
            # Extract text from all pages
            text_content = ""
            total_pages = len(reader.pages)
            
            for page in reader.pages:
                page_text = page.extract_text() or ""
                text_content += ("\n" + page_text)
            
            return text_content, total_pages
            
        except Exception as e:
            raise CVProcessingError(f"Error al extraer texto del PDF: {str(e)}") from e

