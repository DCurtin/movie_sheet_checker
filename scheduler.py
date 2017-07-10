#!/usr/bin/python
from apscheduler.schedulers.blocking import BlockingScheduler
import update_sheet

def update_movies():
    update_sheet.update_list()

scheduler = BlockingScheduler()
scheduler.add_job(update_movies, 'interval', minutes=1)
scheduler.start()
