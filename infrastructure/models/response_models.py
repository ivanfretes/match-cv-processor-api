"""Response models for API endpoints"""
from pydantic import BaseModel
from typing import Optional, List, Dict


class CVResponse(BaseModel):
    """Response model for CV processing"""
    filename: str
    total_pages: int
    character_count: int
    text: str
    message: str
    summary: Optional[str] = None
    summary_generated: bool = False
    summary_error: Optional[str] = None
    
    class Config:
        from_attributes = True


class CSVResponse(BaseModel):
    """Response model for CSV processing"""
    filename: str
    total_rows: int
    columns: List[str]
    data: List[Dict[str, str]]
    
    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str


class RootResponse(BaseModel):
    """Response model for root endpoint"""
    message: str

