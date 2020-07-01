import datetime
import os
import sqlite3
import sys
from collections import deque
from threading import Lock, Timer
import time
import pandas as pd
import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))
os.chdir(os.path.realpath(os.path.dirname(__file__)))

analyzer = SentimentIntensityAnalyzer()


reddit = praw.Reddit(client_id='.........',
                     client_secret='.........', password='........',
                     user_agent='testscript by /u/.....', username='.....')


conn = sqlite3.connect('reddit.db', isolation_level=None,
                       check_same_thread=True)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS threads
             (thread text NOT NULL, sentiment real, time datetime)''')
conn.commit()
conn.close()


class listener():

    def topic(self, text=""):
        return text

    def subred(self, text='worldnews'):
        subreddit = reddit.subreddit(text)
        return subreddit

    def save_in_db(self):

        #subreddit = self.subred()
        #track = self.topic()
        subreddit = reddit.subreddit('all')

        for submis in subreddit.stream.submissions():
            try:
                submission = submis.selftext
                submission = submission.lower()
                vs = analyzer.polarity_scores(submission)["compound"]
                time = datetime.datetime.now()
                values = (submission, vs, time)

                conn = sqlite3.connect('reddit.db')
                c = conn.cursor()
                c.execute(
                    'INSERT OR IGNORE INTO threads (thread,sentiment,time) VALUES (?,?,?)', values)
                conn.commit()

                for comment in subreddit.stream.comments(skip_existing=True):

                    parent_id = str(comment.parent())
                    submission = reddit.comment(parent_id)
                    thread = submission.body
                    thread = thread.lower()
                    vs = analyzer.polarity_scores(submission.body)["compound"]
                    time = datetime.datetime.now()
                    values = (thread, vs, time)

                    c.execute(
                        'INSERT OR IGNORE INTO threads (thread,sentiment,time) VALUES (?,?,?)', values)
                    conn.commit()

                    for reply in submission.replies:
                        reply = reply.lower()
                        vs = analyzer.polarity_scores(reply)["compound"]
                        time = datetime.datetime.now()
                        rep_values = (reply, vs, time)

                        c.execute(
                            'INSERT OR IGNORE INTO threads (thread,sentiment,time) VALUES (?,?,?)', rep_values)
                        conn.commit()

            except praw.exceptions.PRAWException as e:
                #print(e)
                pass

    def del_from_db(self):

        HM_DAYS_KEEP = 30
        current_ms_time = time.time()*1000
        one_day = 86400 * 1000
        del_to = int(current_ms_time - (HM_DAYS_KEEP*one_day))


        conn.execute("DELETE FROM sentiment WHERE unix < {}".format(del_to))
        conn.execute("DELETE FROM threads WHERE thread IS NULL OR trim(thread) = ''")
        conn.execute("VACUUM")
        conn.commit()
        conn.close()


while True:
    try:
        redditlistern = listener()
        redditlistern.save_in_db()
        redditlistern.del_from_db()
    except Exception as e:
        print(str(e))
        time.sleep(5)

Timer(5, redditlistern).start()
