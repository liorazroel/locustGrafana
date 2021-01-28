from requests.exceptions import ReadTimeout


def single_user(locust_client):
    with locust_client.client.get("/api/users?page=2", timeout=1, catch_response=True) as response:
        if response.text == "":
            response.failure("response /api/users?page=2 took over 50ms")
        else:
            response.success()


def single_user_not_found(locust_client):
    response = locust_client.client.get("/api/users/23")
    locust_client.logger.error(response.ok)
