import threading
import time

import schedule

from utility import utility

# Run job everyday at 10:30


def cache_job(token, org, redis):
    schedule.every(15).minutes.do(utility.cache_response, token, org, redis)
    schedule.every(20).minutes.do(utility.cache_analysis, token, org, redis)
    while True:
        print("[RUNNING] cache_job")
        schedule.run_pending()
        time.sleep(60 * 60)


def start_cache_job(token, org, redis):
    # starting cache cron as a separate thread
    t = threading.Thread(
        target=cache_job,
        kwargs={
            "token": token,
            "org": org,
            "redis": redis})
    t.start()
    print("[STARTED] cache_job")
