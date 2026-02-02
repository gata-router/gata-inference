"""Tests for the model module."""

__author__ = "Dave Hall <me@davehall.com.au>"
__copyright__ = "Copyright 2024- 2025, Skwashd Services Pty Ltd https://gata.works"
__license__ = "MIT"

import pytest
import transformers

import src.schemas.schemas
import src.utils.model


@pytest.mark.filterwarnings(
    "ignore::FutureWarning"
)  # This is deep in the tokenizer. We don't control that code
def test_model() -> None:
    """Test the Model class."""
    model = src.utils.model.Model("bert-base-uncased")
    assert isinstance(model, src.utils.model.Model)


@pytest.mark.filterwarnings(
    "ignore::FutureWarning"
)  # This is deep in the tokenizer. We don't control that code
def test_load_config() -> None:
    """Test the load_config method."""
    model = src.utils.model.Model("bert-base-uncased")
    config = model.load_config("bert-base-uncased")
    assert isinstance(config, transformers.BertConfig)


@pytest.mark.filterwarnings(
    "ignore::FutureWarning"
)  # This is deep in the tokenizer. We don't control that code
def test_predict() -> None:
    """Test the predict method."""
    model = src.utils.model.Model("bert-base-uncased")
    prediction = model.predict("this is a test.")
    assert isinstance(prediction, src.schemas.schemas.Prediction)
    assert prediction.label in model.id2label.values()  # type: ignore
    assert prediction.probability >= 0.0
    assert prediction.probability <= 1.0
