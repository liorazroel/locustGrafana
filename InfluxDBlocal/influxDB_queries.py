class InfluxDBQueries:
    @staticmethod
    def insert_request_login(request_type, request_name, response_time):
        insert_request_login = [
            {
                "measurement": "login_requests",
                "tags": {
                    "query": request_type + request_name
                },
                "fields": {
                    "response_time": response_time
                }
            }
        ]

        return insert_request_login
