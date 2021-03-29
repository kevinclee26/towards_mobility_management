from apscheduler.schedulers.blocking import BlockingScheduler
import fetch

sched=BlockingScheduler()
fetch_freq_mins=5

@sched.scheduled_job('interval', minutes=fetch_freq_mins)
def timed_job(): 
	fetch.all_scooter_data()
	fetch.weather_data()
	print(f'This job is run every {fetch_freq_mins} minutes.')
	return None

# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# def scheduled_job():
#     print('This job is run every weekday at 5pm.')

sched.start()