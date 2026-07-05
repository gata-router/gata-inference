"""
Shared test configuration.

src.main loads the model when it is imported. Point it at the base BERT model
before any test module triggers that import.
"""

__author__ = "Dave Hall <me@davehall.com.au>"
__copyright__ = "Copyright 2024 - 2026, Skwashd Services Pty Ltd https://gata.works"
__license__ = "MIT"

import os

os.environ.setdefault("SM_MODEL_DIR", "bert-base-uncased")
