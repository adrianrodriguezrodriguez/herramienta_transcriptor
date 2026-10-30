"""Transcripción y separación de voces, sin servicios externos."""
import os

__version__ = "1.0.0"
for _key in ("HF_HUB_OFFLINE", "TRANSFORMERS_OFFLINE", "HF_HUB_DISABLE_TELEMETRY"):
    os.environ[_key] = "1"
