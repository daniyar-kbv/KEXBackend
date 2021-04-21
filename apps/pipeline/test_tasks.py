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

from requests import get


class TestPropertyTask(Task):
    number = 2
    timeout = 10
    autoretry_for: Tuple[Exception] = (Timeout, HTTPError, ConnectionError)
    max_retries = 3
    default_retry_delay: int = 3

    @property
    def get_number(self):
        self.number = 4
        time.sleep(5)
        return self.number

    @property
    def refresh_number(self):
        self.number = 2
        return self.number

    def run(self, *args, **kwargs):
        try:
            print("sending get request")
            res = get("https://adil.kek.mek")
            print("response:", res)
        except TimeoutError:
            print("timeout error handler is called")
        except HTTPError:
            print("http error handler")
        except ConnectionError:
            print("connection error handler is called")
            self.retry()
            raise ConnectionError

        finally:
            print("finally block is called")
            print("heeyya")

test_property_task = celery_app.register_task(TestPropertyTask())
