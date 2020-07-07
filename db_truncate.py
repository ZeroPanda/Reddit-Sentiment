'''
Run as a cronjob to keep database size under control
'''
import time
import sqlite3

conn = sqlite3.connect('reddit.db', check_same_thread=False)
c = conn.cursor()

HM_DAYS_KEEP = 30
current_ms_time = time.time()*1000
one_day = 86400 * 1000
del_to = int(current_ms_time - (HM_DAYS_KEEP*one_day))

c.execute("DELETE FROM threads WHERE time < {}".format(del_to))
c.execute("DELETE FROM threads WHERE thread IS NULL OR trim(thread) = ''")

conn.isolation_level = None
conn.execute('VACUUM')
conn.isolation_level = ''

conn.commit()
conn.close()
