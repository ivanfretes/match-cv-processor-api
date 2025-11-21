"""Request models for API endpoints"""
from pydantic import BaseModel
from typing import Optional


class ProcessCVRequest(BaseModel):
    """Request model for CV processing"""
    language: str = "spanish"
    generate_summary: bool = True


class ProcessCSVRequest(BaseModel):
    """Request model for CSV processing"""
    pass

