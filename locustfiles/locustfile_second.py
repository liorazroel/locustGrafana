from locust import HttpUser, between, TaskSet, SequentialTaskSet, task
from locust.exception import StopUser
from http_requests.post_requests import *
from http_requests.get_requests import *
import logging
import os

# if not os.path.exists("logs"):
#     os.mkdir("logs")
#
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


#
# f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# f_handler = logging.FileHandler("logs/log" + datetime.now().strftime("%d.%m.%Y_%H-%M") + ".log")
# f_handler.setFormatter(f_format)
# logger.addHandler(f_handler)


class UserBehavior(SequentialTaskSet):
    wait_time = between(1, 2)

    # tasks = [unsuccessful_login]

    def __init__(self, parent):
        super().__init__(parent)
        self.logger = logger
        self.token = None

    @task
    def unsuccessful_login(self):
        unsuccessful_login(self)

    @task
    def login_successful(self):
        self.token = login_successful(self)

    @task
    def single_user(self):
        single_user(self)

    @task
    def single_user_not_found(self):
        single_user_not_found(self)

    # @task
    # def stop_user(self):
    #     raise StopUser()


class WebsiteUser(HttpUser):
    def on_start(self):
        logger.info("starting locust in dev environment...")

    tasks = [UserBehavior]

    def on_stop(self):
        logger.info("finish all!")
