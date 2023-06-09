from typing import Callable

from fastapi import FastAPI
from loguru import logger

from app.core.config import DEFAULT_MODEL_PATH
# from app.services.models import SentimentAnalysisModel
from app.services.models import HeartbeatClassificationModel
from app.services.models_image import HeartbeatClassificationModelImage


def _startup_model(app: FastAPI) -> None:
    model_path = DEFAULT_MODEL_PATH
    model_instance = HeartbeatClassificationModel(model_path)
    model_instance_image = HeartbeatClassificationModelImage(model_path)
    app.state.model = model_instance
    app.state.model_image = model_instance_image


def _shutdown_model(app: FastAPI) -> None:
    app.state.model = None
    app.state.model_image = None


def start_app_handler(app: FastAPI) -> Callable:
    def startup() -> None:
        logger.info("Running app start handler.")
        _startup_model(app)

    return startup


def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        logger.info("Running app shutdown handler.")
        _shutdown_model(app)

    return shutdown
