from datetime import datetime, timezone

import celery

from src.models.reddit_post_model import RedditPostModel


def date_str_to_timestamp(date_str: str) -> float:
    if 'T' in date_str:
        if 'Z' in date_str:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        else:
            dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
    else:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
    return dt.replace(tzinfo=timezone.utc).timestamp()


def add_tasks_to_queue_reddit_user(tasks: celery.local.PromiseProxy, elements: list[RedditPostModel]) -> None:
    for element in elements:
        print(element.author_name)
        tasks.apply_async(args=[element.author_name])


def add_task_to_queue_upload_file(tasks: celery.local.PromiseProxy, elements: list[RedditPostModel]) -> None:
    for element in elements:
        if element.image_url:
            tasks.apply_async(args=[element.filename, element.image_url])
