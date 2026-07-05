"""Tests for the FastAPI application."""

__author__ = "Dave Hall <me@davehall.com.au>"
__copyright__ = "Copyright 2024 - 2026, Skwashd Services Pty Ltd https://gata.works"
__license__ = "MIT"

import fastapi.testclient
import pytest

import src.main

CLIENT = fastapi.testclient.TestClient(src.main.app)


def test_ping() -> None:
    """Test the ping endpoint."""
    response = CLIENT.get("/ping")
    assert response.status_code == 200


@pytest.mark.filterwarnings(
    "ignore::FutureWarning"
)  # This is deep in the tokenizer. We don't control that code
def test_invocations() -> None:
    """Test the invocations endpoint."""
    response = CLIENT.post("/invocations", json={"text": "my laptop keeps crashing"})
    assert response.status_code == 200

    body = response.json()
    prediction = body["prediction"]
    assert isinstance(prediction["label"], str)
    assert prediction["label"] in src.main.MODEL.id2label.values()  # type: ignore
    assert isinstance(prediction["probability"], float)
    assert prediction["probability"] >= 0.0
    assert prediction["probability"] <= 1.0


def test_invocations_rejects_bad_payload() -> None:
    """Test the invocations endpoint rejects a payload without text."""
    response = CLIENT.post("/invocations", json={"wrong": "field"})
    assert response.status_code == 422
