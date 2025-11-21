"""CV entity - Domain model for CV documents"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class CV:
    """Entity representing a CV document"""
    filename: str
    text: str
    total_pages: int
    character_count: int
    summary: Optional[str] = None
    summary_generated: bool = False
    summary_error: Optional[str] = None
    
    def has_summary(self) -> bool:
        """Check if CV has a generated summary"""
        return self.summary is not None and self.summary_generated
    
    def is_valid(self) -> bool:
        """Validate that CV has valid content"""
        return len(self.text.strip()) > 0 and self.character_count > 0

