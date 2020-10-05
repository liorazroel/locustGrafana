from locust import HttpUser, between, TaskSet, events
from Requests.post_requests import *
import logging
from influxdb import InfluxDBClient
from InfluxDB.influxDB_queries import InfluxDBQueries

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.ERROR)
logger = logging.getLogger(__name__)

client = InfluxDBClient(host='localhost', port=8086, database='locustio')
requests_name = ["/api/login"]


@events.request_success.add_listener
def hook_request_success(request_type, name, response_time, response_length):
    if name == requests_name[0]:
        client.write_points(InfluxDBQueries.insert_request_login_success(request_type=request_type, request_name=name,
                                                                         response_time=response_time))


@events.request_failure.add_listener
def hook_request_fail(request_type, name, response_time, response_length, exception):
    if name == requests_name[0]:
        client.write_points(InfluxDBQueries.insert_request_login_fails(request_type=request_type, request_name=name,
                                                                       response_time=response_time,
                                                                       exception=exception))


class UserBehavior(TaskSet):
    wait_time = between(1, 2)
    tasks = [unsuccessful_login, login_successful]

    def __init__(self, parent):
        super().__init__(parent)
        self.logger = logger

    def on_start(self):
        self.logger.info("login user...")
        login_successful(self)

    def unsuccessful_login(self):
        unsuccessful_login(self)

    def login_successful(self):
        login_successful(self)


class WebsiteUser(HttpUser):
    def on_start(self):
        logger.info("starting locust in dev environment...")

    tasks = [UserBehavior]

    def on_stop(self):
        client.close()
