#!/usr/bin/env python3

"""Main app file."""
import os

import uvicorn
from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from routes import router

logger.add(
    "logs/info.log",
    level="INFO",
    rotation="3 days",
    retention="15 days",
    compression="zip",
    enqueue=True,
)

logger.add(
    "logs/debug.log",
    level="DEBUG",
    rotation="3 days",
    retention="15 days",
    compression="zip",
    enqueue=True,
)

logger.add(
    "logs/error.log",
    level="ERROR",
    rotation="3 days",
    retention="15 days",
    compression="zip",
    enqueue=True,
)


if __name__ == "__main__":

    async def on_startup(*args):
        logger.info("Backend init")

    async def on_shutdown(*args):
        pass

    app = FastAPI(title="Cache server")

    app.include_router(router, prefix=f"", tags=["web"])
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=os.getenv("PORT", 7001),
    )
