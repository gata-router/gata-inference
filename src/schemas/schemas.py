"""Schemas for the API."""

__author__ = "Dave Hall <me@davehall.com.au>"
__copyright__ = "Copyright 2024- 2025, Skwashd Services Pty Ltd https://gata.works"
__license__ = "MIT"


from pydantic import BaseModel


class Prediction(BaseModel):
    """Prediction schema."""

    label: str
    probability: float


class Result(BaseModel):
    """Result schema."""

    prediction: Prediction


class Ticket(BaseModel):
    """Ticket schema."""

    text: str
