from packages.otai_hf_local.src import otai_hf_local
from packages.otai_hf_local.src.otai_hf_local import HFLocalTextClassificationPipe
from packages.otai_hf_local.src.otai_hf_local.hf_local_text_classification_pipe import (
    HFLocalTextClassificationPipeConfig,
)


def test_import_hf_local_text_classification_pipe():
    assert HFLocalTextClassificationPipe is not None
    assert HFLocalTextClassificationPipeConfig is not None


def test_import_from_package():
    assert otai_hf_local is not None
