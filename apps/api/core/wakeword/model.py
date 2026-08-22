"""
FRIDAY AI Operating System

Wake Word Model Adapter

This module isolates FRIDAY from the OpenWakeWord API.

Only this file imports openwakeword directly.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np
from openwakeword.model import Model


class WakeWordModel:
    """
    Production wrapper around OpenWakeWord.

    Responsibilities
    ----------------
    • Load wake-word models
    • Validate predictions
    • Return confidence scores
    • Hide OpenWakeWord implementation
    """

    def __init__(
        self,
        model_name: str,
        model_path: Optional[str] = None,
        inference_framework: str = "onnx",
    ):

        self.model_name = model_name

        self.model_path = (
            Path(model_path).resolve()
            if model_path
            else None
        )

        kwargs = {
            "inference_framework": inference_framework
        }

        # If a custom model exists, use it.
        if self.model_path is not None:
            kwargs["wakeword_models"] = [
                str(self.model_path)
            ]

        self._model = Model(**kwargs)

    @property
    def backend(self) -> str:
        return type(self._model).__name__

    def reset(self) -> None:
        """
        Reset internal prediction buffers.
        """
        self._model.reset()

    def predict(self, audio: np.ndarray) -> float:
        """
        Predict wake-word confidence.

        Parameters
        ----------
        audio:
            float32 numpy array sampled at 16 kHz.

        Returns
        -------
        float
            Confidence score between 0 and 1.
        """

        if not isinstance(audio, np.ndarray):
            raise TypeError(
                "Audio must be a numpy.ndarray."
            )

        if audio.dtype != np.float32:
            audio = audio.astype(np.float32)

        predictions = self._model.predict(audio)

        if not isinstance(predictions, dict):
            raise RuntimeError(
                "OpenWakeWord returned an invalid prediction."
            )

        #
        # Built-in model
        #
        if self.model_name in predictions:
            return float(
                predictions[self.model_name]
            )

        #
        # Custom model
        #
        if len(predictions) == 1:
            return float(
                next(iter(predictions.values()))
            )

        #
        # Unknown model
        #
        return 0.0

    def predict_with_debounce(
        self,
        audio: np.ndarray,
        threshold: float,
        debounce: float,
    ) -> float:
        """
        Predict using OpenWakeWord's built-in debounce.
        """

        predictions = self._model.predict(
            audio,
            debounce_time=debounce,
            threshold={
                self.model_name: threshold
            },
        )

        if self.model_name in predictions:
            return float(
                predictions[self.model_name]
            )

        if len(predictions) == 1:
            return float(
                next(iter(predictions.values()))
            )

        return 0.0

    def predict_with_patience(
        self,
        audio: np.ndarray,
        threshold: float,
        patience: int,
    ) -> float:
        """
        Predict using OpenWakeWord's built-in patience filter.
        """

        predictions = self._model.predict(
            audio,
            threshold={
                self.model_name: threshold
            },
            patience={
                self.model_name: patience
            },
        )

        if self.model_name in predictions:
            return float(
                predictions[self.model_name]
            )

        if len(predictions) == 1:
            return float(
                next(iter(predictions.values()))
            )

        return 0.0