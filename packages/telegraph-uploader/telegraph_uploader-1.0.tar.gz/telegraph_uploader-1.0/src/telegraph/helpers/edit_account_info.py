import requests
from telegraph.exceptions.telegraph_exception import TelegraphException

BASE_URL = "https://api.telegra.ph"

def edit_account_info(access_token, short_name=None, author_name=None, author_url=None):
    """
    Edit the information of an existing Telegraph account.
    
    Parameters:
    - access_token (str): Access token of the Telegraph account.
    - short_name (str): Optional, new account name.
    - author_name (str): Optional, new default author name used when creating new articles.
    - author_url (str): Optional, new default profile link opened when users click on the author's name.
    
    Returns:
    - dict: Updated account information if the request is successful.
    
    Raises:
    - TelegraphException: If the API request fails or returns an error.
    """
    url = f"{BASE_URL}/editAccountInfo"
    params = {
        "access_token": access_token,
    }
    if short_name:
        params['short_name'] = short_name
    if author_name:
        params['author_name'] = author_name
    if author_url:
        params['author_url'] = author_url

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        result = response.json()
        
        if not result['ok']:
            raise TelegraphException(result['error'])
        
        return result['result']
    
    except requests.RequestException as e:
        raise TelegraphException(f"Request failed: {str(e)}")