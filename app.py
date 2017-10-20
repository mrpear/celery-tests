import logging
import requests
from time import sleep

from celery import Celery
from flask import Flask, request
from random import randint, uniform

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://guest@rabbit/'
app.config['API_DELAY'] = 0.2

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task(bind=True, retry_backoff=True, acks_late=False)
def add(self, x, y):
    result = x + y
    data = {'result': result}
    try:
        requests.post('http://api:5000/result/', data, timeout=1.5)
    except Exception as exc:
        logger.exception('API request failed with')
        self.retry(exc=exc)


@app.route('/')
def hello_world():
    a, b = randint(0, 1000), randint(0, 1000)
    add.delay(a, b)
    return 'Hello, World!'


@app.route('/result/', methods=['POST'])
def process_result():
    logger.info('Process result %s' % request.data)
    sleep(uniform(0, app.config['API_DELAY']))
    return 'OK'


@app.route('/delay/', methods=['GET', 'POST'])
def set_delay():
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        print(request.data)
        delay = float(request.form.get('delay'))
        app.config['API_DELAY'] = delay
    return 'Delay {}'.format(app.config['API_DELAY'])
