import requests
from telegraph.exceptions.telegraph_exception import TelegraphException

BASE_URL = "https://api.telegra.ph"

def get_page(path, return_content=False):
    """
    Get a Telegraph page.
    
    Parameters:
    - path (str): Path to the Telegraph page (format Title-12-31).
    - return_content (bool): Optional, if true, a content field will be returned in the Page object.
    
    Returns:
    - dict: Information about the page if the request is successful.
    
    Raises:
    - TelegraphException: If the API request fails or returns an error.
    """
    url = f"{BASE_URL}/getPage/{path}"
    params = {
        "return_content": return_content
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        result = response.json()

        if not result['ok']:
            raise TelegraphException(result['error'])

        return result['result']

    except requests.RequestException as e:
        raise TelegraphException(f"Request failed: {str(e)}")