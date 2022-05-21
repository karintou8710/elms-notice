from elms_info_push import main
import settings
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()
scheduler.add_job(main, 'interval', minutes=settings.INTERVAL_MINUTES)
scheduler.start()