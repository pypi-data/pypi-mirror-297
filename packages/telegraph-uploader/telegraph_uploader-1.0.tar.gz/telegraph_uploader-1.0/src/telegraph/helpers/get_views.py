import requests
from telegraph.exceptions.telegraph_exception import TelegraphException

BASE_URL = "https://api.telegra.ph"

def get_views(path, year=None, month=None, day=None, hour=None):
    """
    Get the number of views for a Telegraph page.
    
    Parameters:
    - path (str): Path to the Telegraph page (format Title-12-31).
    - year (int): Optional, year for which to retrieve views.
    - month (int): Optional, month for which to retrieve views (required if day is passed).
    - day (int): Optional, day for which to retrieve views (required if hour is passed).
    - hour (int): Optional, hour for which to retrieve views.
    
    Returns:
    - dict: Number of views for the page if the request is successful.
    
    Raises:
    - TelegraphException: If the API request fails or returns an error.
    """
    url = f"{BASE_URL}/getViews/{path}"
    params = {}
    
    if year:
        params["year"] = year
    if month:
        params["month"] = month
    if day:
        params["day"] = day
    if hour:
        params["hour"] = hour

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        result = response.json()

        if not result['ok']:
            raise TelegraphException(result['error'])

        return result['result']

    except requests.RequestException as e:
        raise TelegraphException(f"Request failed: {str(e)}")