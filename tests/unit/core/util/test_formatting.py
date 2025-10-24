from open_ticket_ai.core._util.formatting import prettify


def test_prettify_nested_dict():
    nested_dict = {"level1": {"level2": {"level3": "value"}}}
    result = prettify(nested_dict)
    original_str = str(nested_dict)
    assert len(result) > len(original_str)
    assert "\n" in result
