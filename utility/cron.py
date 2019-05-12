import schedule 
import time
import utility
import threading

# overriding the thread implementation to include args
class ScheduleCache(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    def run(self):
        self._target(*self._args)

# Run job everyday at 10:30
def cache_job(token, org, redis):
    schedule.every().day.at("10:30").do(utility.cache_response, token, org, redis)
    while True:
        print("[RUNNING] cache_job")
        schedule.run_pending()
        time.sleep(60*60)
def start_cache_job(token, org, redis):
    # starting cache cron as a separate thread
    t = ScheduleCache(cache_job, token, org, redis)
    t.start()
    print("[STARTED] cache_job")


