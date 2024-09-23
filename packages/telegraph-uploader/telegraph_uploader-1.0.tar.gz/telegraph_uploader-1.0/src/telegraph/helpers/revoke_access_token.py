import requests
from telegraph.exceptions.telegraph_exception import TelegraphException

BASE_URL = "https://api.telegra.ph"

def revoke_access_token(access_token):
    """
    Revoke the current access token and generate a new one for a Telegraph account.
    
    Parameters:
    - access_token (str): Access token of the Telegraph account.
    
    Returns:
    - dict: Account information with the new access token if the request is successful.
    
    Raises:
    - TelegraphException: If the API request fails or returns an error.
    """
    url = f"{BASE_URL}/revokeAccessToken"
    params = {
        "access_token": access_token,
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