def single_user(locust_client):
    response = locust_client.client.get("/api/users?page=2")
    locust_client.logger.info(response.status_code)


def single_user_not_found(locust_client):
    response = locust_client.client.get("/api/users/23")
    locust_client.logger.info(response.status_code)