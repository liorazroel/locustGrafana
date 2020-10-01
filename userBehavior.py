from locust import TaskSet, between


def login(locust_client):
    locust_client.client.post("/api/login", {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    })


class UserBehavior(TaskSet):
    wait_time = between(1, 2)

    def on_start(self):
        login(self)
