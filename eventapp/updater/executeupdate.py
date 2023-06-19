from apscheduler.schedulers.background import BackgroundScheduler
from .updater import create_save

def execute():
    scheduler = BackgroundScheduler()
    scheduler.add_job(create_save, trigger = "interval", minutes = 1)
    scheduler.start()
