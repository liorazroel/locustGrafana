def login_successful(locust_client):
    response = locust_client.client.post("/api/login", json={
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    })

    locust_client.logger.info(response.text)


def unsuccessful_login(locust_client):
    response = locust_client.client.post("/api/login", json={
        "email": "peter@klaven"
    })

    locust_client.logger.info(response.status_code)
