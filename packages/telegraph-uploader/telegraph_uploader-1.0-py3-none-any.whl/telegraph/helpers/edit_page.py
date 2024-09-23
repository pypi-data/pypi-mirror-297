import requests
from telegraph.exceptions.telegraph_exception import TelegraphException

BASE_URL = "https://api.telegra.ph"

def edit_page(access_token, path, title, content, author_name=None, author_url=None, return_content=False):
    """
    Edit an existing Telegraph page.
    
    Parameters:
    - access_token (str): Access token of the Telegraph account.
    - path (str): Path to the page (format Title-12-31).
    - title (str): New title for the page.
    - content (list): New content of the page in Node format (Array of Node).
    - author_name (str): Optional, new author name displayed below the title.
    - author_url (str): Optional, new profile link opened when users click on the author's name.
    - return_content (bool): Optional, if true, a content field will be returned in the Page object.
    
    Returns:
    - dict: Information about the edited page if the request is successful.
    
    Raises:
    - TelegraphException: If the API request fails or returns an error.
    """
    url = f"{BASE_URL}/editPage/{path}"
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