import logging

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from app_config import AppConfig
from dds_loader.dds_message_processor_job import DdsMessageProcessor

app = Flask(__name__)

config = AppConfig()


@app.get('/health')
def hello_world():
    return 'healthy'
 

if __name__ == '__main__':
    app.logger.setLevel(logging.DEBUG)

    config = AppConfig()

    consumer = config.kafka_consumer()
    producer = config.kafka_producer()
    postgres_db = config.pg_warehouse_db()
 
    proc = DdsMessageProcessor(consumer, producer, postgres_db, batch_size=100, logger=app.logger)

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=proc.run, trigger="interval", seconds=config.DEFAULT_JOB_INTERVAL)
    scheduler.start()

    app.run(debug=True, host='0.0.0.0', use_reloader=False)
