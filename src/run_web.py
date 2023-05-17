#!/usr/bin/env python3

"""Main app file."""
import json
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

    app = FastAPI(title="Cache server")

    async def on_startup(*args):
        logger.info("Backend init")
        storage = {}
        try:
            with open("./cache/.overview.json", "r") as f:
                storage = json.load(f)
        except:
            pass
        app.extra["storage"] = storage

    async def on_shutdown(*args):
        with open("./cache/.overview.json", "w") as f:
            json.dump(app.extra.get("storage"), f)
        logger.info("overview.json saved")

    app.include_router(router, prefix=f"", tags=["web"])
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler("startup", on_startup)
    app.add_event_handler("shutdown", on_shutdown)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=os.getenv("PORT", 7001),
    )
