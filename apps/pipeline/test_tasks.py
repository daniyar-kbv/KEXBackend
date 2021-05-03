import time
import random

from celery import Task

from config import celery_app
import time
from copy import deepcopy
from typing import Optional, Type, Tuple, Dict, Union

from celery import Task
from requests import Session
from requests.models import Response
from requests.exceptions import HTTPError, ConnectionError, Timeout


class TestTask(Task):
    number = 1

    def run(self, *args, **kwargs):
        print("self number is:", self.number)
        self.number = random.randint(2, 100)
        print("new number is:", self.number)
        time.sleep(5)
        self.test_method()

    def test_method(self):
        print('printing number in test_method', self.number)

test_task = celery_app.register_task(TestTask())

from requests import post


class TestPropertyTask(Task):
    count = 0

    def run(self, count=0):
        print(count)
        url="http://192.168.1.194:8000/apply-ticket-insurance/schedule"
        data = {
            "principal": 250000,
            "period": 6,
            "product": "AVIATA",
        }
        res = post(url, json=data)
        print("res:", res)


test_property_task = celery_app.register_task(TestPropertyTask())
