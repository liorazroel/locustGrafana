from locust import HttpUser, HttpLocust
from userBehavior import UserBehavior
import logging


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
