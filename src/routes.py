import datetime
import os

import aiohttp
from fastapi import APIRouter
from loguru import logger
from starlette.requests import Request
from starlette.responses import RedirectResponse

router = APIRouter()


def clean_storage(storage, maxsize=10000):
    items = list(storage.items())
    for name, _ in sorted(items, key=lambda x: x[1]):
        if len(storage) < maxsize:
            return

        cache_path = os.path.join("./cache", name)
        if os.path.exists(cache_path):
            logger.info(f"Removing {name}")
            os.remove(cache_path, )
        storage.pop(name, None)


@router.get("/{path:path}")
async def redirect_to_cache(
    r: Request,
    path: str,
):
    name = path.replace("/", "-")
    cache_path = os.path.join("./cache", name)
    if not os.path.exists(cache_path):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"https://{path}") as response:
                    if response.status == 200:
                        with open(cache_path, "wb") as f:
                            f.write(await response.read())
                        logger.info(
                            f"Image {path} downloaded and saved to the cache folder."
                        )
                    else:
                        logger.info(f"Failed to download image from {path}")
                        return RedirectResponse(url=f"https://{path}")
            except Exception as e:
                logger.error(f"{e} {path}")

    r.app.extra["storage"][name] = datetime.datetime.utcnow().timestamp()
    clean_storage(r.app.extra["storage"], maxsize=10000)
    return RedirectResponse(url=f"https://storage.herewallet.app/cache/{name}")
