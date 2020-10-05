class InfluxDBQueries:
    @staticmethod
    def insert_request_login_success(request_type, request_name, response_time):
        insert_request_login_success = [
            {
                "measurement": "login_requests",
                "tags": {
                    "query": request_type + request_name,
                    "is_fail": False
                },
                "fields": {
                    "response_time": response_time,
                    "error": None
                }
            }
        ]

        return insert_request_login_success

    @staticmethod
    def insert_request_login_fails(request_type, request_name, response_time, exception):
        insert_request_login_fails = [
            {
                "measurement": "login_requests",
                "tags": {
                    "query": request_type + request_name,
                    "is_fail": True
                },
                "fields": {
                    "response_time": response_time,
                    "error": str(exception)
                }
            }
        ]

        return insert_request_login_fails
