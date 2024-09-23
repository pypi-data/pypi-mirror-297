from telegraph.helpers.create_account import create_account
from telegraph.helpers.edit_account_info import edit_account_info
from telegraph.helpers.get_account_info import get_account_info
from telegraph.helpers.revoke_access_token import revoke_access_token
from telegraph.helpers.create_page import create_page
from telegraph.helpers.edit_page import edit_page
from telegraph.helpers.get_page import get_page
from telegraph.helpers.get_page_list import get_page_list
from telegraph.helpers.get_views import get_views

class TelegraphAPI:
    def __init__(self, access_token=None):
        self.access_token = access_token

    def create_account(self, short_name, author_name="", author_url=""):
        return create_account(short_name, author_name, author_url)

    def edit_account_info(self, short_name=None, author_name=None, author_url=None):
        return edit_account_info(self.access_token, short_name, author_name, author_url)

    def get_account_info(self, fields=None):
        return get_account_info(self.access_token, fields)

    def revoke_access_token(self):
        result = revoke_access_token(self.access_token)
        self.access_token = result.get('access_token')
        return result

    def create_page(self, title, content, author_name=None, author_url=None, return_content=False):
        return create_page(self.access_token, title, content, author_name, author_url, return_content)

    def edit_page(self, path, title, content, author_name=None, author_url=None, return_content=False):
        return edit_page(self.access_token, path, title, content, author_name, author_url, return_content)

    def get_page(self, path, return_content=False):
        return get_page(path, return_content)

    def get_page_list(self, offset=0, limit=50):
        return get_page_list(self.access_token, offset, limit)

    def get_views(self, path, year=None, month=None, day=None, hour=None):
        return get_views(path, year, month, day, hour)