def test_import_hf_local_text_classification_pipe():
    from otai_hf_local.hf_local_text_classification_pipe import (
        HFLocalTextClassificationPipe,
        HFLocalTextClassificationPipeConfig,
    )

    assert HFLocalTextClassificationPipe is not None
    assert HFLocalTextClassificationPipeConfig is not None


def test_import_from_package():
    import otai_hf_local

    assert otai_hf_local is not None
