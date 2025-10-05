"""
Example: Custom Template Extensions

This example demonstrates how to extend JinjaRenderer with custom template
methods and variables using decorators.
"""

from open_ticket_ai.core.template_rendering import (
    jinja_template_method,
    jinja_variable,
)
from open_ticket_ai.core.template_rendering.jinja_renderer import JinjaRenderer


@jinja_template_method("format_priority")
def format_priority(priority: int) -> str:
    """Format a numeric priority as a human-readable string."""
    priority_map = {
        1: "🟢 Low",
        2: "🟡 Medium",
        3: "🟠 High",
        4: "🔴 Critical",
    }
    return priority_map.get(priority, "❓ Unknown")


@jinja_template_method("shorten")
def shorten(text: str, max_length: int = 50) -> str:
    """Shorten text to a maximum length."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


@jinja_template_method("ticket_url")
def ticket_url(ticket_id: str, base_url: str = "https://tickets.example.com") -> str:
    """Generate a URL for a ticket."""
    return f"{base_url}/ticket/{ticket_id}"


@jinja_variable("ticket_statuses")
def get_ticket_statuses() -> dict[str, str]:
    """Provide a map of ticket status codes to descriptions."""
    return {
        "new": "New Ticket",
        "open": "Open",
        "pending": "Pending Customer Response",
        "resolved": "Resolved",
        "closed": "Closed",
    }


@jinja_variable("system_config")
def get_system_config() -> dict[str, str]:
    """Provide system-wide configuration values."""
    return {
        "support_email": "support@example.com",
        "max_attachment_size_mb": "10",
        "ticket_prefix": "TKT",
    }


def demo() -> None:
    """Demonstrate the custom template extensions."""
    renderer = JinjaRenderer()

    print("=== Custom Template Method Examples ===\n")

    template1 = "Priority: {{ format_priority(3) }}"
    result1 = renderer.render(template1, {})
    print(f"Template: {template1}")
    print(f"Result:   {result1}\n")

    template2 = "{{ shorten('This is a very long text that needs to be shortened', 30) }}"
    result2 = renderer.render(template2, {})
    print(f"Template: {template2}")
    print(f"Result:   {result2}\n")

    template3 = "URL: {{ ticket_url('12345') }}"
    result3 = renderer.render(template3, {})
    print(f"Template: {template3}")
    print(f"Result:   {result3}\n")

    print("=== Custom Variable Examples ===\n")

    template4 = "Status: {{ ticket_statuses.open }}"
    result4 = renderer.render(template4, {})
    print(f"Template: {template4}")
    print(f"Result:   {result4}\n")

    template5 = "Contact us at {{ system_config.support_email }}"
    result5 = renderer.render(template5, {})
    print(f"Template: {template5}")
    print(f"Result:   {result5}\n")

    print("=== Combined Example ===\n")

    template6 = """
Ticket {{ system_config.ticket_prefix }}-12345:
Priority: {{ format_priority(4) }}
Status: {{ ticket_statuses.resolved }}
View: {{ ticket_url('12345') }}
""".strip()
    result6 = renderer.render(template6, {})
    print(f"Template:\n{template6}\n")
    print(f"Result:\n{result6}\n")


if __name__ == "__main__":
    demo()
