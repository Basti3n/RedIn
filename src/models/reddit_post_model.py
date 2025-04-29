import re
from dataclasses import dataclass, InitVar, field
from datetime import datetime

from bs4.element import Tag


@dataclass
class RedditPostModel:
    article: InitVar[Tag]
    permalink: str = field(init=False)
    title: str = field(init=False)
    author_id: str = field(init=False)
    author_name: str = field(init=False)
    timestamp: float = field(init=False)
    score: int = field(init=False)
    comments: int = field(init=False)
    image_url: str = field(init=False)
    image_name: str = field(init=False)
    filename: str = field(init=False)

    def __post_init__(self, article: Tag) -> None:
        details = article.find('shreddit-post')
        self.title = details.get('post-title')
        self.author_id = details.get('author-id')
        self.author_name = details.get('author')
        self.timestamp = datetime.strptime(details.get('created-timestamp'), "%Y-%m-%dT%H:%M:%S.%f%z").timestamp()
        self.permalink = details.get('permalink')
        self.score = int(details.get('score'))
        self.comments = int(details.get('comment-count'))
        img = article.find('img', {'srcset': True})
        self.image_url = img.get('src') if img else None
        self.filename = re.search(r'/([^/?]+)(?=\?)', self.image_url).group(1) if self.image_url else None
