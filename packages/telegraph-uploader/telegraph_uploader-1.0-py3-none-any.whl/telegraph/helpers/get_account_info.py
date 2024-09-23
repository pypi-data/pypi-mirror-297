import requests
from telegraph.exceptions.telegraph_exception import TelegraphException

BASE_URL = "https://api.telegra.ph"

def get_account_info(access_token, fields=None):
    """
    Get information about a Telegraph account.
    
    Parameters:
    - access_token (str): Access token of the Telegraph account.
    - fields (list): Optional, list of account fields to return. Defaults to ["short_name", "author_name", "author_url"].
    
    Returns:
    - dict: Account information if the request is successful.
    
    Raises:
    - TelegraphException: If the API request fails or returns an error.
    """
    url = f"{BASE_URL}/getAccountInfo"
    params = {
        "access_token": access_token,
        "fields": fields or ["short_name", "author_name", "author_url"]
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