import requests
from telegraph.exceptions.telegraph_exception import TelegraphException

BASE_URL = "https://api.telegra.ph"

def get_page_list(access_token, offset=0, limit=50):
    """
    Get a list of pages belonging to a Telegraph account.
    
    Parameters:
    - access_token (str): Access token of the Telegraph account.
    - offset (int): Sequential number of the first page to be returned. Default is 0.
    - limit (int): Limits the number of pages to be retrieved. Default is 50, max is 200.
    
    Returns:
    - dict: List of pages if the request is successful.
    
    Raises:
    - TelegraphException: If the API request fails or returns an error.
    """
    url = f"{BASE_URL}/getPageList"
    params = {
        "access_token": access_token,
        "offset": offset,
        "limit": limit
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