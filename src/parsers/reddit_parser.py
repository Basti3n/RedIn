from dataclasses import dataclass, field
from io import BytesIO
from typing import Any

import niquests
from bs4 import BeautifulSoup
from bs4.element import Tag

from src.models.reddit_post_model import RedditPostModel
from src.models.reddit_user_model import RedditUserModel
from src.request_handler import RequestHandler


@dataclass
class RedditParser:
    _base_url: str
    request_handler: RequestHandler
    _headers: dict[str, str] = field(init=False)

    def __post_init__(self) -> None:
        self._headers = {
            'accept-language': 'fr-FR,fr;q=0.7',
            'sec-gpc': '1',
            'upgrade-insecure-requests': '1'
        }

    def parse_first_page(self, sub_reddit: str) -> tuple[list[RedditPostModel], str]:
        full_url = f'{self._base_url}/r/{sub_reddit}/new/'
        print(f'Parsing sub reddit `{sub_reddit}`: {full_url}')

        request = self.request_handler.get(full_url, headers=self._headers)
        soup = BeautifulSoup(request.content, 'html.parser')
        articles_list = soup.find_all('article')

        url_next_page = soup.find('faceplate-partial', {'id': 'feed-next-page-partial'}).get('src')

        return self._parse_post(articles_list), url_next_page

    def parse_next_page(self, url_all_next_page: str) -> tuple[list[RedditPostModel], str]:
        request_all = self.request_handler.get(f'{self._base_url}{url_all_next_page}/', headers=self._headers)
        soup = BeautifulSoup(request_all.content, 'html.parser')
        url_next_page = soup.find('faceplate-partial', {'id': 'feed-next-page-partial'}).get('src')
        return self._parse_post(soup.find_all('article')), url_next_page

    @staticmethod
    def _parse_post(posts_list: list[Tag]) -> list[RedditPostModel]:
        return [RedditPostModel(post) for post in posts_list]

    def parse_a_reddit_user(self, username: str) -> dict[str, Any]:
        user_url = f'{self._base_url}/user/{username}'
        request = niquests.get(user_url, headers=self._headers)
        print(f'Parsing username `{username}`: {user_url}')
        soup = BeautifulSoup(request.content, 'html.parser')
        return RedditUserModel(soup).__dict__

    def get_image(self, url: str) -> tuple[int, BytesIO]:
        response = self.request_handler.get(url)

        image_data = BytesIO(response.content)
        image_size = len(response.content)
        return image_size, image_data
