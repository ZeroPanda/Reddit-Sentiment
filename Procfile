web: gunicorn app:server
worker: celery worker --app=tasks.app
senti1: python reddit_stream.py
cleaner: python db_truncate.py