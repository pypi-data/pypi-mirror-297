import requests
from telegraph.exceptions.telegraph_exception import TelegraphException

BASE_URL = "https://api.telegra.ph"

def create_account(short_name, author_name="", author_url=""):
    """
    Create a new Telegraph account.
    
    Parameters:
    - short_name (str): Account name, helps users with several accounts remember which they are using.
    - author_name (str): Optional, default author name used when creating new articles.
    - author_url (str): Optional, default profile link opened when users click on the author's name.
    
    Returns:
    - dict: Account information if the request is successful.
    
    Raises:
    - TelegraphException: If the API request fails or returns an error.
    """
    url = f"{BASE_URL}/createAccount"
    params = {
        "short_name": short_name,
        "author_name": author_name,
        "author_url": author_url
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