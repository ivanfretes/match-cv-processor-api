"""CSV Document entity - Domain model for CSV files"""
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class CSVDocument:
    """Entity representing a CSV document"""
    filename: str
    total_rows: int
    columns: List[str]
    data: List[Dict[str, str]]
    
    def is_valid(self) -> bool:
        """Validate that CSV has valid content"""
        return len(self.columns) > 0 and self.total_rows >= 0

