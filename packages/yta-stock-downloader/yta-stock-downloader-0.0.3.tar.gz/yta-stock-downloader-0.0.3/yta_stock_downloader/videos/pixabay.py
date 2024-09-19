from yta_general_utils.downloader.video import download_video
from yta_general_utils.programming.env import get_current_project_env

import urllib.parse
import requests


PIXABAY_API_KEY = get_current_project_env('PIXABAY_API_KEY')

def __get_url(query):
    params = {
        'key': PIXABAY_API_KEY,
        'q': query,
        'pretty': 'true'
    }

    return 'https://pixabay.com/api/videos/?' + urllib.parse.urlencode(params)

def download_first(query, output_filename):
    """
    Downloads the first available video found with the provided search 'query'.
    It is downloaded in the maximun quality available and stored with the
    'output_filename' provided.
    """
    response = requests.get(__get_url(query), timeout = 10)
    response = response.json()

    if response['total'] == 0:
        return None
    
    # TODO: Check 'output_filename' is valid

    # By now I return the first result found
    videos = response['hits'][0]['videos']

    # I dinamically detect the best quality to download
    if 'large' in videos:
        url = videos['large']['url']
    elif 'medium' in videos:
        url = videos['medium']['url']
    elif 'small' in videos:
        url = videos['small']['url']
    elif 'tiny' in videos:
        url = videos['tiny']['url']

    return download_video(url, output_filename)

    """
    for video in response['hits']:
        return 
        qualities = video['videos']
        # Qualities come in order, so get the first one by now and thats all
    print(response)

    # response.hits.videos.large,medium,small,tiny
    """
