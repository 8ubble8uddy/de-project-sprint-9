import logging

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from app_config import AppConfig
from cdm_loader.cdm_message_processor_job import CdmMessageProcessor


app = Flask(__name__)

config = AppConfig()


@app.get('/health')
def hello_world():
    return 'healthy'
 

if __name__ == '__main__':
    app.logger.setLevel(logging.DEBUG)

    consumer = config.kafka_consumer()
    postgres_db = config.pg_warehouse_db()

    proc = CdmMessageProcessor(consumer, postgres_db, batch_size=100, logger=app.logger)

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=proc.run, trigger="interval", seconds=config.DEFAULT_JOB_INTERVAL)
    scheduler.start()

    app.run(debug=True, host='0.0.0.0', use_reloader=False)
