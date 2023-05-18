import datetime
import os
from io import BytesIO
from typing import Optional
from urllib.parse import quote

import aiohttp
import yaml
from fastapi import APIRouter
from loguru import logger
from starlette.requests import Request
from starlette.responses import RedirectResponse
from PIL import Image
import pngquant


router = APIRouter()

with open("config.yml", "r") as config_file:
    CONFIG = yaml.safe_load(config_file)


def get_folder_size(folder_path):
    """
    Calculates the total size of a folder in megabytes.

    Args:
        folder_path (str): The path to the folder.

    Returns:
        float: The size of the folder in megabytes.
    """
    total_size = 0
    for path, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(path, file)
            total_size += os.path.getsize(file_path)
    return total_size / 1024 / 1024


def resize_image_async(image_data, target_width):
    image = Image.open(BytesIO(image_data))
    original_width, original_height = image.size
    aspect_ratio = original_width / original_height

    resized_image = image.resize((int(target_width), int(target_width / aspect_ratio)))
    output_buffer = BytesIO()
    resized_image.save(output_buffer, format="PNG")
    resized_image_data = output_buffer.getvalue()
    return resized_image_data


def clean_storage(storage, max_size=10000):
    """
    Cleans up the storage by removing items if the maximum size is exceeded.

    Args:
        storage (dict): The storage dictionary.
        max_size (int): The maximum size of the storage.

    Returns:
        None
    """
    if len(storage) < max_size:
        return

    items = sorted(storage.items(), key=lambda x: x[1])
    for name, _ in items:
        if len(storage) < max_size:
            storage["folder_size"] = get_folder_size(CONFIG["cache_folder"])
            logger.info(f'folder_size: {storage["folder_size"]}')
            return

        cache_path = os.path.join(CONFIG["cache_folder"], name)
        if os.path.exists(cache_path):
            logger.info(f"Removing {name}")
            os.remove(cache_path)
        storage.pop(name, None)


@router.get("/{path:path}")
async def redirect_to_cache(r: Request, path: str, sz: Optional[int] = None):
    """
    Endpoint to redirect requests to cached images.
    Args:
        r (Request): The incoming request.
        path (str): The path to the image.
    Returns:
        RedirectResponse: The redirect response.
    """

    url_path = quote(path)
    folder_size = r.app.extra["storage"].get("folder_size", 0)
    if folder_size > CONFIG["folder_size"]:
        logger.error("Not enough memory to cache images")
        return RedirectResponse(url=f"https://{path}")

    name = path.replace("/", "-")
    url_name = url_path.replace("/", "-")
    cache_path = os.path.join(CONFIG["cache_folder"], name)

    if not os.path.exists(cache_path):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"https://{url_path}") as response:
                    if response.status == 200:
                        with open(cache_path, "wb") as f:
                            image = await response.read()
                            f.write(image)
                            pngquant.quant_image(cache_path, cache_path, 90)

                        logger.info(
                            f"Image {path} downloaded and saved to the cache folder."
                        )
                    else:
                        logger.info(f"Failed to download image from {path}")
                        return RedirectResponse(url=f"https://{url_path}")
            except Exception as e:
                logger.exception(e)
                logger.error(f"{e} {url_path}")
                return RedirectResponse(url=f"https://{url_path}")

    if sz:
        name = f"{sz}-" + name
        url_name = f"{sz}-" + url_name

        rs_cache_path = os.path.join(CONFIG["cache_folder"], name)
        if not os.path.exists(rs_cache_path):
            with open(cache_path, "rb") as f:
                image = resize_image_async(f.read(), int(sz))
            with open(rs_cache_path, "wb") as f:
                f.write(image)

    r.app.extra["storage"][name] = datetime.datetime.utcnow().timestamp()
    clean_storage(r.app.extra["storage"], max_size=CONFIG["max_size"])
    return RedirectResponse(url=f"{CONFIG['image_server_prefix']}{url_name}")
