"""FastAPI application for serving Gata model."""

__author__ = "Dave Hall <me@davehall.com.au>"
__copyright__ = "Copyright 2024- 2025, Skwashd Services Pty Ltd https://gata.works"
__license__ = "MIT"


import logging
import os

from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse

import src.schemas.schemas
import src.utils.model

logger = logging.getLogger(__name__)

logger.setLevel(int(os.environ.get("SM_LOG_LEVEL", logging.INFO)))

# Load the model and tokenizer on startup
SM_MODEL_DIR = os.environ.get("SM_MODEL_DIR", "/opt/ml/model")
MODEL = src.utils.model.Model(SM_MODEL_DIR)

app = FastAPI()


@app.get("/ping")
async def ping() -> Response:
    """Handle request to the ping endpoint."""
    return Response(
        status_code=status.HTTP_200_OK,
    )


@app.post("/invocations")
async def invocations(ticket: src.schemas.schemas.Ticket) -> Response:
    """Handle a prediction request from SageMaker."""
    prediction = MODEL.predict(ticket.text)
    result = src.schemas.schemas.Result(prediction=prediction)

    return JSONResponse(
        content=result.model_dump(),
        status_code=status.HTTP_200_OK,
        media_type="application/json",
    )
