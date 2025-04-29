from dataclasses import dataclass, InitVar, field
from datetime import datetime

from bs4 import BeautifulSoup


@dataclass
class RedditUserModel:
    soup: InitVar[BeautifulSoup]
    user_id: str = field(init=False)
    username: str = field(init=False)
    creation_date: datetime = field(init=False)

    def __post_init__(self, soup: BeautifulSoup) -> None:
        pass
        self.user_id = soup.find('shreddit-overflow-menu').get('author-id')
        self.username = soup.find('shreddit-overflow-menu').get('author-name')
        creation_date_str = soup.find('time', {'data-testid': 'cake-day'}).get('datetime')
        self.creation_date = datetime.fromisoformat(creation_date_str.replace('Z', '+00:00'))
