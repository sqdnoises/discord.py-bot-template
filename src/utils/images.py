"""
Image-related utilities.
"""

from io     import BytesIO
from typing import (
    TYPE_CHECKING, Optional
)

from .bot import get_raw_content_data

import aiohttp
import numpy as np
from PIL             import Image
from PIL.Image       import Image as PILImage
from sklearn.cluster import KMeans

__all__ = (
    "fetch_image",
    "get_dominant_color"
)

async def fetch_image(image_url: str, *args, session: Optional[aiohttp.ClientSession] = None, **kwargs) -> PILImage:
    """
    Fetches an image from a URL asynchronously and returns a PIL Image object.

    Args:
        image_url (str): The URL of the image to fetch.
        session (Optional[aiohttp.ClientSession]): An optional aiohttp ClientSession to use for the request.
            If not provided, a new session will be created.
        
    Returns:
        PILImage: The image object.
    """
    
    image_data = await get_raw_content_data(image_url, *args, session=session, **kwargs)
    return Image.open(BytesIO(image_data)).convert("RGBA")

def get_dominant_color(image: Image.Image) -> tuple[int, int, int]:
    """
    Processes a PIL Image object and extracts the most bright and dominant color
    from the entire image, excluding transparent pixels.

    Args:
        image (Image.Image): A PIL Image object to process.

    Returns:
        Tuple[int, int, int]: The RGB values of the bright and dominant color.
    """
    # Convert the image to a numpy array
    pixels = np.array(image)

    # Mask out transparent pixels (alpha channel == 0)
    if pixels.shape[-1] == 4:  # Check if image has an alpha channel
        non_transparent_pixels = pixels[pixels[..., 3] > 0]  # Keep non-transparent pixels
    else:
        non_transparent_pixels = pixels  # Assume all pixels are non-transparent if no alpha channel

    # If there are no non-transparent pixels, return a default value (e.g., white)
    if non_transparent_pixels.shape[0] == 0:
        return (255, 255, 255)  # Default to white if no non-transparent pixels

    # Convert RGBA to RGB (remove alpha channel) and reshape the array for clustering
    pixels_rgb = non_transparent_pixels[..., :3].reshape(-1, 3)

    # Calculate brightness for each pixel using luminance (perceptual model)
    # Luminance formula: 0.2126*R + 0.7152*G + 0.0722*B
    brightness = 0.2126 * pixels_rgb[:, 0] + 0.7152 * pixels_rgb[:, 1] + 0.0722 * pixels_rgb[:, 2]

    # Filter to keep the top 25% brightest pixels for clustering
    threshold = np.percentile(brightness, 75)  # 75th percentile brightness
    bright_pixels = pixels_rgb[brightness >= threshold]

    # If there are no bright pixels, fall back to clustering all pixels
    if bright_pixels.shape[0] == 0:
        bright_pixels = pixels_rgb

    # Apply KMeans to find the most prominent bright color
    kmeans = KMeans(n_clusters=1, random_state=0)
    kmeans.fit(bright_pixels)

    if TYPE_CHECKING:  # epic gaslighting right here
        dominant_color: tuple[int, int, int] = (0, 0, 0)
    else:
        dominant_color = tuple(map(int, kmeans.cluster_centers_[0]))  # Get the dominant color and convert it into integers
    
    return dominant_color