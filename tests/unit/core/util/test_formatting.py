from open_ticket_ai.core.util.formatting import prettify


def test_prettify_nested_dict():
    nested_dict = {"level1": {"level2": {"level3": "value"}}}
    result = prettify(nested_dict)
    assert len(result) > 50
    assert "\n" in result
