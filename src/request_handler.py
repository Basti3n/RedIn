import random
from dataclasses import dataclass, InitVar
from time import sleep
from typing import Any

import niquests
from bs4 import BeautifulSoup


@dataclass
class RequestHandler:
    dict_settings: InitVar[dict[str, Any]]

    def __post_init__(self, dict_settings: dict[str, Any]) -> None:
        self._user_agents = dict_settings['user-agents']

    def _add_user_agent_to_headers(self, headers: dict[str, Any]) -> dict[str, Any]:
        if headers is None:
            headers = {}
        headers['User-Agent'] = random.choice(self._user_agents)
        return headers

    def get(self, url: str, headers: dict[str, Any] = None, retry: int = 3) -> niquests.Response:
        print(f'GET {url} | try `{retry}`')
        print(headers)
        retry -= 1
        headers_updated = self._add_user_agent_to_headers(headers)
        response = niquests.get(url=url, headers=headers_updated, allow_redirects=True)
        soup = BeautifulSoup(response.content, 'html.parser')
        next_page = soup.find('faceplate-partial', {'id': 'feed-next-page-partial'})

        if response.status_code == 200 and next_page is not None:
            return response
        else:
            if retry == 0:
                response.raise_for_status()
            else:
                sleep(1)
                return self.get(url, headers, retry)
