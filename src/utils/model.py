"""BERT model manager."""

__author__ = "Dave Hall <me@davehall.com.au>"
__copyright__ = "Copyright 2024- 2025, Skwashd Services Pty Ltd https://gata.works"
__license__ = "MIT"


import torch
from transformers import (
    BertConfig,
    BertForSequenceClassification,
    BertTokenizer,
    TextClassificationPipeline,
)

from src.schemas.schemas import Prediction


class Model:
    """BERT model manager."""

    def __init__(self, model_path: str) -> None:
        """
        Initialize the model manager.

        Args:
        ----
          model_path: The path to the model.

        """
        config = self.load_config(model_path)
        self.id2label = config.id2label

        model = self.load_model(model_path, config)
        tokenizer = self.load_tokenizer(model_path)
        self.classifier = TextClassificationPipeline(model=model, tokenizer=tokenizer)

    def load_config(self, model_path: str) -> BertConfig:
        """
        Load the model configuration.

        Args:
        ----
          model_path: The path to the model.

        Returns:
        -------
          The model configuration.

        """
        config = BertConfig.from_pretrained(model_path)
        config.local_files_only = True
        return config

    def load_model(
        self, model_path: str, config: BertConfig
    ) -> BertForSequenceClassification:
        """
        Load the model from disk.

        Args:
        ----
          model_path: The path to the model.
          config: The model configuration.

        Returns:
        -------
          The model.

        """
        model = BertForSequenceClassification.from_pretrained(model_path, config=config)
        model.eval()

        return model

    def load_tokenizer(self, model_path: str) -> BertTokenizer:
        """
        Load the tokenizer.

        Args:
        ----
          model_path: The path to the model.

        Returns:
        -------
          The tokenizer.

        """
        return BertTokenizer.from_pretrained(model_path)

    @torch.no_grad()
    def predict(self, text: str) -> Prediction:
        """
        Predicts the labels for a given input text.

        Args:
        ----
          text: The input text.

        Returns:
        -------
          The predicted label and its probability.

        """
        outputs = self.classifier(text, truncation=True)

        return Prediction(
            label=str(outputs[0]["label"]),
            probability=outputs[0]["score"],
        )
