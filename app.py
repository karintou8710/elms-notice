from elms_info_push import main
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()
scheduler.add_job(main, 'interval', seconds=10)
scheduler.start()