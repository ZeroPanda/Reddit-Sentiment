from celery import Celery
import reddit_stream

app = celery.Celery('tasks', broker='redis://localhost:6379')
import os
app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])
@app.task
def getApp():
  return reddit_stream
