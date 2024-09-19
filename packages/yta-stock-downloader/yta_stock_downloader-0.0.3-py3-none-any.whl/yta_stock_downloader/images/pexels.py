from yta_general_utils.downloader.image import download_image
from yta_general_utils.programming.env import get_current_project_env
from yta_stock_downloader.images.pexels_image import PexelsImage
from yta_stock_downloader.images.constants import PEXELS_SEARCH_IMAGE_API_ENDPOINT_URL
from yta_stock_downloader.images.pexels_image_page_result import PexelsImagePageResult

import requests


PEXELS_API_KEY = get_current_project_env('PEXELS_API_KEY')

HEADERS = {
    'content-type': 'application/json',
    'Accept-Charset': 'UTF-8',
    'Authorization': PEXELS_API_KEY
}

def search_pexels_images(query: str, locale: str = 'es-ES', per_page: int = 25, page: int = 1) -> PexelsImagePageResult:
    """
    Makes a search of Pexels images and returns the results.
    """
    params = {
        'query': query,
        'orientation': 'landscape',   # landscape | portrait | square
        'size': 'large',   # large | medium | small
        'locale': locale, # 'es-ES' | 'en-EN' ...
        'per_page': per_page,
        'page': page
    }
    response = requests.get(PEXELS_SEARCH_IMAGE_API_ENDPOINT_URL, params = params, headers = HEADERS)
    page_results = PexelsImagePageResult(query, locale, response.json())

    return page_results

def get_first_pexels_image(query: str, locale: str = 'es-ES') -> PexelsImage:
    """
    Returns the first existing image (if existing) for the provided
    'keywords'.

    The result will be None if no results, or an object that 
    contains the 'id', 'width', 'height', 'url'
    """
    if not query:
        return None
    
    if not locale:
        return None
    
    results = search_pexels_images(query, locale, 1)

    if not results:
        return None
    
    return results[0]

def download_first_pexels_image(query, output_filename) -> str:
    image_to_download = get_first_pexels_image(query)

    downloaded = download_image(image_to_download.src['landscape'], output_filename)

    # TODO: Maybe make 'download_image' to return the downloaded file name
    # or None if not downloaded that is a better way of working
    if not downloaded:
        return None

    return output_filename