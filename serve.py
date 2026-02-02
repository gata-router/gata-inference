#!/usr/bin/env python3
"""SageMaker entry point."""

__author__ = "Dave Hall <me@davehall.com.au>"
__copyright__ = "Copyright 2024- 2025, Skwashd Services Pty Ltd https://gata.works"
__license__ = "MIT"


import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",  # noqa:S104 SageMaker needs the container to bind to all interfaces
        port=8080,
        log_level="info",
    )
