import os
from typing import Any

from celery import Celery

from src.file_manager import FileManager
from src.minio_manager import MinioManager
from src.parsers.reddit_parser import RedditParser
from src.request_handler import RequestHandler
from src.utils import date_str_to_timestamp, add_tasks_to_queue_reddit_user, add_task_to_queue_upload_file

s_path = os.path.abspath(__file__)
settings_manager = FileManager(s_path, 'settings.json')

broker_url = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
minio_endpoint = os.environ.get('MINIO_ENDPOINT', 'localhost:9000')

app = Celery('tasks', broker=broker_url, backend=broker_url)

request_handler = RequestHandler(settings_manager.file_content['request_handler'])
reddit_parser = RedditParser(settings_manager.file_content['reddit']['base_url'], request_handler)
minio_client = MinioManager(minio_endpoint, settings_manager.file_content['minio'])


@app.task
def crawl_until_date_reddit_worker(sub_reddit: str, date_until_str: str) -> int:
    print(f'Crawling {sub_reddit} until {date_until_str}')

    date_until = date_str_to_timestamp(date_until_str)

    posts, url_next_page = reddit_parser.parse_first_page(sub_reddit)
    number_of_posts = len(posts)

    add_tasks_to_queue_reddit_user(parse_a_reddit_user, posts)
    add_task_to_queue_upload_file(uploading_picture_to_minio, posts)

    max_date = max(post.timestamp for post in posts)

    while max_date > date_until:
        posts, url_next_page = reddit_parser.parse_next_page(url_next_page)
        number_of_posts += len(posts)

        add_tasks_to_queue_reddit_user(parse_a_reddit_user, posts)
        add_task_to_queue_upload_file(uploading_picture_to_minio, posts)

        max_date = max(post.timestamp for post in posts)

    return number_of_posts


@app.task
def crawl_until_page_reddit_worker(sub_reddit: str, page_end: int) -> int:
    print(f'Crawling {sub_reddit} until page {page_end}')
    posts, url_next_page = reddit_parser.parse_first_page(sub_reddit)
    number_of_posts = len(posts)

    add_tasks_to_queue_reddit_user(parse_a_reddit_user, posts)
    add_task_to_queue_upload_file(uploading_picture_to_minio, posts)

    for page in range(0, page_end + 1):
        posts, url_next_page = reddit_parser.parse_next_page(url_next_page)
        number_of_posts += len(posts)

        add_tasks_to_queue_reddit_user(parse_a_reddit_user, posts)
        add_task_to_queue_upload_file(uploading_picture_to_minio, posts)

    return number_of_posts


@app.task
def parse_a_reddit_user(username: str) -> dict[str, Any]:
    print(f'Parsing Reddit user {username}')
    return reddit_parser.parse_a_reddit_user(username)


@app.task
def uploading_picture_to_minio(filename: str, image_url: str) -> None:
    print(f'Uploading picture `{image_url}` to minio')
    image_size, image_data = reddit_parser.get_image(image_url)
    minio_client.upload_file_from_memory(filename, image_size, image_data)