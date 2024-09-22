class GoPersonalException(Exception):
    """Base exception for GoPersonal SDK"""
    pass

class InitializationError(GoPersonalException):
    """Raised when there's an error during initialization"""
    pass

class APIError(GoPersonalException):
    """Raised when there's an error in API calls"""
    pass
