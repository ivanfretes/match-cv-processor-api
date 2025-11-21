"""Domain exceptions"""


class DomainException(Exception):
    """Base exception for domain layer"""
    pass


class InvalidFileError(DomainException):
    """Raised when file validation fails"""
    pass


class CVProcessingError(DomainException):
    """Raised when CV processing fails"""
    pass


class CSVProcessingError(DomainException):
    """Raised when CSV processing fails"""
    pass

