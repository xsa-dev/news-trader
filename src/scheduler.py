from apscheduler.schedulers.background import BackgroundScheduler
from agent import get_prices
from agents.news.agent import main
# from agents.sentiment.agent import sentiment

scheduler = BackgroundScheduler()
scheduler.add_job(get_prices, 'cron', minute='0,15,30,45', hour='*')
scheduler.add_job(main, 'cron', minute='30', hour='*')
# scheduler.add_job(sentiment, 'cron', hour='*')
scheduler.start()

# ...
print('all task scheduled')


try:
    while True:
        pass
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
