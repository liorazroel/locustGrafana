from locust import HttpUser, between, TaskSet, events,stats
from http_requests.post_requests import *
from http_requests.get_requests import *
import logging
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import os
import env_file

if not os.path.exists("logs"):
    os.mkdir("logs")

env_file.load(".env")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler = logging.FileHandler("logs/log" + datetime.now().strftime("%d.%m.%Y_%H-%M") + ".log")
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)

token = os.getenv("TOKEN")
org = os.getenv("ORG")
bucket = os.getenv("BUCKET")

client = InfluxDBClient(url="https://us-west-2-1.aws.cloud2.influxdata.com", token=token)
requests_name = ["/api/login", "/api/users?page=2", "/api/users/23"]


@events.request_success.add_listener
def hook_request_success(request_type, name, response_time, response_length):
    if name == requests_name[0]:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        data = "requests_login,query=" + request_type + name + " response_time=" + str(response_time)
        write_api.write(bucket, org, data)
    if name == requests_name[1]:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        data = "requests_single_user,query=" + request_type + "/api/users?page_equal_two" + " response_time=" + str(
            response_time)
        write_api.write(bucket, org, data)
    elif name == requests_name[2]:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        data = "requests_single_user,query=" + request_type + "/api/users?page_equal_twenty_three" + " response_time=" + str(
            response_time)
        write_api.write(bucket, org, data)


@events.request_failure.add_listener
def hook_request_fail(request_type, name, response_time, response_length, exception):
    if name == requests_name[0]:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        data = "requests_login,query=" + request_type + name + " response_time=" + str(response_time)
        write_api.write(bucket, org, data)
    if name == requests_name[1]:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        data = "requests_single_user,query=" + request_type + "/api/users?page_equal_two" + " response_time=" + str(
            response_time)
        write_api.write(bucket, org, data)
    elif name == requests_name[2]:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        data = "requests_single_user,query=" + request_type + "/api/users?page_equal_twenty_three" + " response_time=" + str(
            response_time)
        write_api.write(bucket, org, data)


class UserBehavior(TaskSet):
    wait_time = between(1, 2)
    tasks = [unsuccessful_login, login_successful, single_user, single_user_not_found]

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

    def single_user(self):
        single_user(self)

    def single_user_not_found(self):
        single_user_not_found(self)


class WebsiteUser(HttpUser):
    def on_start(self):
        logger.info("starting locust in dev environment...")

    tasks = [UserBehavior]

    def on_stop(self):
        client.close()