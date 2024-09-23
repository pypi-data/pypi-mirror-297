
# Telegraph API Python Library

This Python library provides easy-to-use functions to interact with the [Telegraph API](https://telegra.ph/api), 
which allows you to create, edit, and manage Telegraph posts and accounts.

## Features
- Create and manage Telegraph accounts.
- Create, edit, and retrieve pages.
- Fetch page view statistics.
- Revoke access tokens.
- Easily integrate with any Python project.

## Installation
You can install the required dependencies using `pip`. Make sure you have Python installed.

```bash
pip install Telegraph-Uploader
```

## Usage

Below is an example of how you can use the Telegraph API with this library.

```python
from telegraph import TelegraphAPI

# Initialize API
telegraph_api = TelegraphAPI()

# Create a new account
account = telegraph_api.create_account(short_name="TestUser", author_name="Anonymous", author_url="https://example.com")
print(f"Account created: {account}")

# Access token for future requests
access_token = account['access_token']

# Initialize API with access token
telegraph_api = TelegraphAPI(access_token)

# Create a new page
content = [{"tag": "p", "children": ["This is a sample Telegraph page created via API."]}]
page = telegraph_api.create_page(title="Sample Page", content=content, author_name="Anonymous", return_content=True)
print(f"Page created: {page}")

# Fetch the page details
fetched_page = telegraph_api.get_page(page['path'], return_content=True)
print(f"Fetched page: {fetched_page}")
```

## Methods

### Account Management
- `create_account(short_name, author_name=None, author_url=None)`: Creates a new Telegraph account.
- `edit_account_info(short_name=None, author_name=None, author_url=None)`: Updates account information.
- `get_account_info(fields=None)`: Retrieves account information.
- `revoke_access_token()`: Revokes the current access token and generates a new one.

### Page Management
- `create_page(title, content, author_name=None, author_url=None, return_content=False)`: Creates a new Telegraph page.
- `edit_page(path, title, content, author_name=None, author_url=None, return_content=False)`: Edits an existing page.
- `get_page(path, return_content=False)`: Fetches details of a specific page.
- `get_page_list(offset=0, limit=50)`: Retrieves a list of pages belonging to the account.

### Page Statistics
- `get_views(path, year=None, month=None, day=None, hour=None)`: Gets the number of views for a Telegraph page.

## Error Handling
All errors returned by the Telegraph API are handled by raising `TelegraphException`. For example:

```python
from telegraph.exceptions import TelegraphException

try:
    account = telegraph_api.create_account(short_name="TestUser")
except TelegraphException as e:
    print(f"An error occurred: {e}")
```

## License
This project is licensed under the MIT License.