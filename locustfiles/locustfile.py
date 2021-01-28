from locust import HttpUser, between, TaskSet
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
