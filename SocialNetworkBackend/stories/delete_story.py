from apscheduler.schedulers.background import BackgroundScheduler
from .views import delete_expired_stories


def delete():
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_expired_stories,
                      'interval', minutes=1, id='delete-story',
                      replace_existing=True)
    scheduler.start()

