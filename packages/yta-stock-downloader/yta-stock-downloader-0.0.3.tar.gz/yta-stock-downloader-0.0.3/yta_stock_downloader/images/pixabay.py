from yta_general_utils.downloader.image import download_image
from yta_general_utils.programming.env import get_current_project_env

import urllib.parse
import requests


PIXABAY_API_KEY = get_current_project_env('PIXABAY_API_KEY')

def __get_url(query):
    params = {
        'key': PIXABAY_API_KEY,
        'q': query,
        'image_type': 'photo'
    }

    return 'https://pixabay.com/api/?' + urllib.parse.urlencode(params)

def download_first(query, output_filename):
    """
    Downloads the first available image found with the provided seach 'query'.
    It is downloaded in the maxium quality available and stored with the 
    'output_filename' provided.
    """
    response = requests.get(__get_url(query), timeout = 10)
    response = response.json()

    # TODO: Check 'output_filename' is valid

    if response['total'] == 0:
        return None
    
    image = response['hits'][0]
    url = image['largeImageURL']

    return download_image(url, output_filename)