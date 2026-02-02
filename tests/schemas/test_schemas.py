"""Test the schemas module."""

__author__ = "Dave Hall <me@davehall.com.au>"
__copyright__ = "Copyright 2024- 2025, Skwashd Services Pty Ltd https://gata.works"
__license__ = "MIT"

import src.schemas.schemas


def test_prediction() -> None:
    """Test the Prediction class."""
    prediction = src.schemas.schemas.Prediction(
        label="LABEL",
        probability=0.5,
    )
    assert prediction.label == "LABEL"
    assert prediction.probability == 0.5


def test_result() -> None:
    """Test the Result class."""
    prediction = src.schemas.schemas.Prediction(
        label="almost_perfect",
        probability=0.9999,
    )
    result = src.schemas.schemas.Result(
        prediction=prediction,
    )
    assert result.prediction == prediction


def test_ticket() -> None:
    """Test the Ticket class."""
    ticket = src.schemas.schemas.Ticket(
        text="text",
    )
    assert ticket.text == "text"
