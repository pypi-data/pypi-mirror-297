import requests
from telegraph.exceptions.telegraph_exception import TelegraphException

BASE_URL = "https://api.telegra.ph"

def create_page(access_token, title, content, author_name=None, author_url=None, return_content=False):
    """
    Create a new Telegraph page.
    
    Parameters:
    - access_token (str): Access token of the Telegraph account.
    - title (str): Title of the page.
    - content (list): Content of the page in Node format (Array of Node).
    - author_name (str): Optional, author name displayed below the article's title.
    - author_url (str): Optional, profile link opened when users click on the author's name.
    - return_content (bool): Optional, if true, a content field will be returned in the Page object.
    
    Returns:
    - dict: Information about the created page if the request is successful.
    
    Raises:
    - TelegraphException: If the API request fails or returns an error.
    """
    url = f"{BASE_URL}/createPage"
    params = {
        "access_token": access_token,
        "title": title,
        "content": content,
        "return_content": return_content
    }
    if author_name:
        params["author_name"] = author_name
    if author_url:
        params["author_url"] = author_url

    try:
        response = requests.post(url, json=params)
        response.raise_for_status()
        result = response.json()

        if not result['ok']:
            raise TelegraphException(result['error'])

        return result['result']

    except requests.RequestException as e:
        raise TelegraphException(f"Request failed: {str(e)}")