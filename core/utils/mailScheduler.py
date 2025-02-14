from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
jobstores = {'schedulers_store': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')}
scheduler = BackgroundScheduler(jobstores=jobstores, job_defaults={'misfire_grace_time': 20},)
scheduler.start()