import threading
import time

import schedule

from utility import utility

# Run job everyday at 10:30


def cache_job(token, org, redis):
    utility.cache_analysis(token, org, redis)
    schedule.every().day.at("10:30").do(utility.cache_response, token, org, redis)
    schedule.every().day.at("07:21").do(utility.cache_analysis, token, org, redis)
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
