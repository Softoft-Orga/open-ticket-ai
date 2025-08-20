from pydantic import BaseModel


class EmptyDataModel(BaseModel):
    """Empty Pydantic model without any fields.

    This model serves as a placeholder for scenarios requiring a Pydantic-compatible
    object but without any data fields. It can be used as a base class or type hint
    when no specific data structure is needed.

    Example:
        ```python
        # Using as a type hint for API responses with no content
        def empty_response() -> EmptyDataModel:
            return EmptyDataModel()
        ```

    Note:
        Inherits all base functionality from `pydantic.BaseModel` while maintaining
        an empty field structure.
    """
    pass