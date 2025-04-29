from celery import Celery

app = Celery(broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')


# Crawl based on page
result = app.send_task('tasks.crawl_until_page_reddit_worker', args=['uniqlo', 3])
print(result.get())

# Crawl based on date
# result = app.send_task('tasks.crawl_until_date_reddit_worker', args=['uniqlo', '2025-02-25'])
# print(result.get())