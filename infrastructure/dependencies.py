"""Dependency injection for API endpoints"""
from fastapi import Depends
from openai import OpenAI
from infrastructure.config.config import config
from infrastructure.adapters.openai_adapter import OpenAIAdapter
from infrastructure.adapters.pypdf_extractor import PyPDFExtractor
from infrastructure.adapters.text_cleaner_adapter import TextCleanerAdapter
from infrastructure.adapters.csv_reader_adapter import CSVReaderAdapter
from application.use_cases.process_cv_use_case import ProcessCVUseCase
from application.use_cases.process_csv_use_case import ProcessCSVUseCase
from domain.ports.llm_service_port import LLMServicePort
from domain.ports.pdf_extractor_port import PDFExtractorPort
from domain.ports.text_cleaner_port import TextCleanerPort
from domain.ports.csv_reader_port import CSVReaderPort


def get_llm_service() -> LLMServicePort:
    """
    Dependency injection for LLM service
    
    Returns:
        LLMServicePort implementation (OpenAIAdapter)
    """
    api_key = config.get_required("OPENAI_API_KEY")
    model = config.get("OPENAI_MODEL", "gpt-3.5-turbo")
    return OpenAIAdapter(api_key=api_key, model=model)


def get_pdf_extractor() -> PDFExtractorPort:
    """
    Dependency injection for PDF extractor
    
    Returns:
        PDFExtractorPort implementation (PyPDFExtractor)
    """
    return PyPDFExtractor()


def get_text_cleaner() -> TextCleanerPort:
    """
    Dependency injection for text cleaner
    
    Returns:
        TextCleanerPort implementation (TextCleanerAdapter)
    """
    return TextCleanerAdapter()


def get_csv_reader() -> CSVReaderPort:
    """
    Dependency injection for CSV reader
    
    Returns:
        CSVReaderPort implementation (CSVReaderAdapter)
    """
    return CSVReaderAdapter()


def get_process_cv_use_case(
    pdf_extractor: PDFExtractorPort = Depends(get_pdf_extractor),
    text_cleaner: TextCleanerPort = Depends(get_text_cleaner),
    llm_service: LLMServicePort = Depends(get_llm_service)
) -> ProcessCVUseCase:
    """
    Dependency injection for ProcessCVUseCase
    
    Args:
        pdf_extractor: PDF extractor service
        text_cleaner: Text cleaner service
        llm_service: LLM service for summary generation
        
    Returns:
        ProcessCVUseCase instance
    """
    return ProcessCVUseCase(
        pdf_extractor=pdf_extractor,
        text_cleaner=text_cleaner,
        llm_service=llm_service
    )


def get_process_csv_use_case(
    csv_reader: CSVReaderPort = Depends(get_csv_reader)
) -> ProcessCSVUseCase:
    """
    Dependency injection for ProcessCSVUseCase
    
    Args:
        csv_reader: CSV reader service
        
    Returns:
        ProcessCSVUseCase instance
    """
    return ProcessCSVUseCase(csv_reader=csv_reader)

