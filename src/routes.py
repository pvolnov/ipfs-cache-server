import os

import aiohttp
from fastapi import APIRouter
from loguru import logger
from starlette.responses import RedirectResponse

router = APIRouter()


@router.get("/{path:path}")
async def redirect_to_cache(
    path: str,
):
    name = path.replace("/", "-")
    cache_path = os.path.join("./cache", name)
    if not os.path.exists(cache_path):
        async with aiohttp.ClientSession() as session:
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

    return RedirectResponse(url=f"https://storage.herewallet.app/cache/{name}")
