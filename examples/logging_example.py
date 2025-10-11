"""Example demonstrating usage of the abstract logging service.

This example shows how to:
1. Use the LoggingModule with dependency injection
2. Inject a LoggerFactory into a service
3. Use the logger with context binding
4. Switch between stdlib and structlog implementations via environment variable
"""

from __future__ import annotations

from injector import Injector, inject

from open_ticket_ai.core.dependency_injection.logging_module import LoggingModule
from open_ticket_ai.core.logging_iface import LoggerFactory


class UserService:
    """Example service that uses the abstract logging interface."""

    @inject
    def __init__(self, logger_factory: LoggerFactory):
        """Initialize the service with a logger factory.

        Args:
            logger_factory: Factory for creating loggers
        """
        self._logger = logger_factory.get_logger(
            self.__class__.__name__,
            service="user_service",
            version="1.0",
        )

    def create_user(self, user_id: str, username: str) -> None:
        """Create a new user.

        Args:
            user_id: The user's ID
            username: The user's username
        """
        logger = self._logger.bind(user_id=user_id, operation="create_user")

        logger.info("Creating user", username=username)

        try:
            logger.debug("Validating user data")

            logger.info("User created successfully")
        except Exception as e:
            logger.exception("Failed to create user", error=str(e))
            raise

    def update_user(self, user_id: str, email: str) -> None:
        """Update a user's email.

        Args:
            user_id: The user's ID
            email: The new email address
        """
        logger = self._logger.bind(user_id=user_id, operation="update_user")

        logger.info("Updating user email", email=email)

        logger.warning("Email update requires verification")

        logger.info("User updated successfully")


def main() -> None:
    """Demonstrate logging with both stdlib and structlog implementations."""
    print("\n" + "=" * 60)
    print("Using stdlib logging (default)")
    print("=" * 60)

    injector_stdlib = Injector([LoggingModule(log_impl="stdlib", log_level="DEBUG")])
    service_stdlib = injector_stdlib.get(UserService)

    service_stdlib.create_user("user_123", "alice")
    service_stdlib.update_user("user_123", "alice@example.com")

    print("\n" + "=" * 60)
    print("Using structlog")
    print("=" * 60)

    injector_structlog = Injector([LoggingModule(log_impl="structlog", log_level="DEBUG")])
    service_structlog = injector_structlog.get(UserService)

    service_structlog.create_user("user_456", "bob")
    service_structlog.update_user("user_456", "bob@example.com")

    print("\n" + "=" * 60)
    print("Example completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
