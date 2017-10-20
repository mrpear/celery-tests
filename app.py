from celery import Celery
from flask import Flask
from random import randint

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://guest@rabbit/'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task
def add(x, y):
    return x + y


@app.route('/')
def hello_world():
    a, b = randint(0, 1000), randint(0, 1000)
    add.delay(a, b)
    return 'Hello, World!'
