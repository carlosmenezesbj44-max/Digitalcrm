class CRMException(Exception):
    """Base exception for CRM errors."""
    pass


class NotFoundException(CRMException):
    """Raised when a resource is not found."""
    pass


class ValidationException(CRMException):
    """Raised when validation fails."""
    pass


class AuthenticationException(CRMException):
    """Raised when authentication fails."""
    pass


class AuthorizationException(CRMException):
    """Raised when authorization fails."""
    pass


class DatabaseException(CRMException):
    """Raised when database operations fail."""
    pass
