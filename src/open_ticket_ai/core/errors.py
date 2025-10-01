
class OpenTicketAIError(Exception):
    """Base exception for all custom exceptions in the Open Ticket AI application."""

    pass


# Configuration Errors
class ConfigurationError(OpenTicketAIError):
    """Base exception for configuration-related errors."""

    pass


class MissingConfigurationError(ConfigurationError):
    """Raised when a required configuration is missing."""

    pass


class InvalidConfigurationError(ConfigurationError):
    """Raised when a configuration value is invalid."""

    pass


class EnvironmentVariableError(ConfigurationError):
    """Raised when there's an issue with environment variables."""

    pass


# Pipeline Errors
class PipelineError(OpenTicketAIError):
    """Base exception for pipeline-related errors."""

    pass


class PipelineExecutionError(PipelineError):
    """Raised when there's an error during pipeline execution."""

    pass


class PipelineValidationError(PipelineError):
    """Raised when pipeline validation fails."""

    pass


class PipelineTimeoutError(PipelineError):
    """Raised when a pipeline operation times out."""

    pass


# Template Processing Errors
class TemplateError(OpenTicketAIError):
    """Base exception for template-related errors."""

    pass


class TemplateSyntaxError(TemplateError):
    """Raised when there's a syntax error in a template."""

    pass


class TemplateRenderingError(TemplateError):
    """Raised when there's an error rendering a template."""

    pass


class UndefinedVariableError(TemplateError):
    """Raised when an undefined variable is accessed in a template."""

    pass


# Data Processing Errors
class DataProcessingError(OpenTicketAIError):
    """Base exception for data processing errors."""

    pass


class DataValidationError(DataProcessingError):
    """Raised when data validation fails."""

    pass


class DataTransformationError(DataProcessingError):
    """Raised when data transformation fails."""

    pass


# API Errors
class APIError(OpenTicketAIError):
    """Base exception for API-related errors."""

    pass


class APIConnectionError(APIError):
    """Raised when there's a connection error with an external API."""

    pass


class APIResponseError(APIError):
    """Raised when an API returns an error response."""

    pass


class APIRateLimitExceeded(APIError):
    """Raised when API rate limits are exceeded."""

    pass


# Authentication & Authorization Errors
class AuthenticationError(OpenTicketAIError):
    """Base exception for authentication errors."""

    pass


class UnauthorizedError(AuthenticationError):
    """Raised when a user is not authorized to perform an action."""

    pass


class InvalidCredentialsError(AuthenticationError):
    """Raised when invalid credentials are provided."""

    pass


# File Operations Errors
class FileOperationError(OpenTicketAIError):
    """Base exception for file operation errors."""

    pass


class FileNotFoundError(FileOperationError):
    """Raised when a file is not found."""

    pass


class FilePermissionError(FileOperationError):
    """Raised when there's a permission error with file operations."""

    pass


# Database Errors
class DatabaseError(OpenTicketAIError):
    """Base exception for database-related errors."""

    pass


class DatabaseConnectionError(DatabaseError):
    """Raised when there's an error connecting to the database."""

    pass


class DatabaseQueryError(DatabaseError):
    """Raised when there's an error executing a database query."""

    pass


# Validation Errors
class ValidationError(OpenTicketAIError):
    """Base exception for validation errors."""

    pass


class InvalidInputError(ValidationError):
    """Raised when input data is invalid."""

    pass


class MissingRequiredFieldError(ValidationError):
    """Raised when a required field is missing."""

    pass


# AI/ML Related Errors
class AIProcessingError(OpenTicketAIError):
    """Base exception for AI/ML processing errors."""

    pass


class ModelLoadingError(AIProcessingError):
    """Raised when there's an error loading an AI model."""

    pass


class PredictionError(AIProcessingError):
    """Raised when there's an error during model prediction."""

    pass


# Network Errors
class NetworkError(OpenTicketAIError):
    """Base exception for network-related errors."""

    pass


class ConnectionTimeoutError(NetworkError):
    """Raised when a network connection times out."""

    pass


class ServiceUnavailableError(NetworkError):
    """Raised when a required service is unavailable."""

    pass
