from locust import HttpUser, between, TaskSet, events
from Requests.post_requests import *
import logging
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.ERROR)
logger = logging.getLogger(__name__)

token = "FDjCD5hijcxdpdw-1Itkcw-tfhwdtOBoqbSIHUcJMW6CjJ1uTv03j--krxK76tADhCNFwMW4hzjZFKqBAvgb7w=="
org = "lior4332@gmail.com"
bucket = "locustio"

client = InfluxDBClient(url="https://us-west-2-1.aws.cloud2.influxdata.com", token=token)


@events.request_success.add_listener
def hook_request_success(request_type, name, response_time, response_length):
    write_api = client.write_api(write_options=SYNCHRONOUS)
    data = "requests,query=" + request_type + name + " response_time=" + str(response_time)
    write_api.write(bucket, org, data)


@events.request_failure.add_listener
def hook_request_fail(request_type, name, response_time, response_length, exception):
    write_api = client.write_api(write_options=SYNCHRONOUS)
    data = "bad_requests,query=" + request_type + name + " response_time=" + str(response_time)
    write_api.write(bucket, org, data)


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




