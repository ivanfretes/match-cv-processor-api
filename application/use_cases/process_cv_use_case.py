"""Use case for processing CV PDF files"""
from typing import Optional
from domain.entities.cv import CV
from domain.ports.pdf_extractor_port import PDFExtractorPort
from domain.ports.text_cleaner_port import TextCleanerPort
from domain.ports.llm_service_port import LLMServicePort
from domain.exceptions.domain_exceptions import CVProcessingError


class ProcessCVUseCase:
    """Use case for processing CV PDF files and optionally generating summaries"""
    
    def __init__(
        self,
        pdf_extractor: PDFExtractorPort,
        text_cleaner: TextCleanerPort,
        llm_service: Optional[LLMServicePort] = None
    ):
        """
        Initialize the use case
        
        Args:
            pdf_extractor: Service for extracting text from PDFs
            text_cleaner: Service for cleaning extracted text
            llm_service: Optional service for generating summaries
        """
        self.pdf_extractor = pdf_extractor
        self.text_cleaner = text_cleaner
        self.llm_service = llm_service
    
    async def execute(
        self,
        file_content: bytes,
        filename: str,
        language: str = "spanish",
        generate_summary: bool = True
    ) -> CV:
        """
        Execute the CV processing use case
        
        Args:
            file_content: PDF file content as bytes
            filename: Original filename
            language: Language for summary generation (spanish/english)
            generate_summary: Whether to generate a summary using LLM
            
        Returns:
            CV entity with processed data
            
        Raises:
            CVProcessingError: If processing fails
        """
        try:
            # Extract text from PDF
            text_content, total_pages = await self.pdf_extractor.extract_text(
                file_content, filename
            )
            
            # Clean and normalize the text
            cleaned_text = self.text_cleaner.clean(text_content)
            
            # Count characters after cleaning
            character_count = len(cleaned_text)
            
            # Create CV entity
            cv = CV(
                filename=filename,
                text=cleaned_text,
                total_pages=total_pages,
                character_count=character_count,
                summary=None,
                summary_generated=False
            )
            
            # Generate summary if requested and LLM service is available
            if generate_summary and cleaned_text.strip() and self.llm_service:
                try:
                    summary = await self.llm_service.generate_cv_summary(
                        cv_text=cleaned_text,
                        language=language
                    )
                    cv.summary = summary
                    cv.summary_generated = True
                    cv.summary_error = None
                except Exception as e:
                    # If summary generation fails, continue without summary
                    cv.summary = None
                    cv.summary_generated = False
                    cv.summary_error = str(e)
            
            return cv
            
        except Exception as e:
            raise CVProcessingError(f"Error al procesar el CV: {str(e)}") from e

