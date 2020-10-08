from prometheus_client import start_http_server, Metric
import time
import requests
import json
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

url = "http://localhost:8089/stats/requests"

locust_status = {"ready": 0, "spawning": 1, "running": 2, "stopped": 3, "not_connected": 4}


class LocustCollector:
    @staticmethod
    def collect():
        try:
            response = requests.get(url).content.decode('Utf-8')
        except requests.exceptions.ConnectionError:
            logger.error("Failed to connect to Locust with url: " + url)
            response = None
            metric = Metric("locust_status", "State of the locust host web ui", 'gauge')
            metric.add_sample("locust_status", value=locust_status["not_connected"], labels={'state': "Not connected"})
            yield metric

        if response is not None:
            response_json = json.loads(response)
            logger.info("response data: " + str(response_json))

            metric = Metric("locust_status", "State of the locust host web ui", 'gauge')
            metric.add_sample("locust_status", value=locust_status[response_json['state']],
                              labels={'state': response_json['state']})
            yield metric

            if response_json['current_response_time_percentile_95'] is not None and response_json['state'] != 'ready':
                logger.info("report to promethues server the num of failures of the test...")
                metric = Metric('num_failures', 'num of failures of http_requests', 'gauge')
                metric.add_sample('num_failures', value=response_json["stats"][len(response_json["stats"]) - 1]["num_failures"], labels={})
                yield metric

                logger.info("report to promethues the average of response time...")
                metric = Metric('avg_response_time', "average of response time", 'gauge')
                metric.add_sample('avg_response_time', value=response_json["stats"][len(response_json["stats"]) - 1]["avg_response_time"], labels={})
                yield metric

                logger.info("report to promethues the number of total http_requests...")
                metric = Metric("num_requests", "Total number of http_requests", 'gauge')
                metric.add_sample("num_requests", value=response_json["stats"][len(response_json["stats"]) - 1]["num_requests"], labels={})
                yield metric

                logger.info("report to promethues the minimum response time of request...")
                metric = Metric("min_response_time", "The minimum response time of request", 'gauge')
                metric.add_sample("min_response_time",
                                  value=response_json["stats"][len(response_json["stats"]) - 1]["min_response_time"],
                                  labels={})
                yield metric

                logger.info("report to promethues the maximum response time of request...")
                metric = Metric("max_response_time", "The maximum response time of request", 'gauge')
                metric.add_sample("max_response_time",
                                  value=response_json["stats"][len(response_json["stats"]) - 1]["max_response_time"],
                                  labels={})
                yield metric

                logger.info("report to promethues the errors of http_requests...")
                metric = Metric('locust_errors', 'Locust http_requests errors', 'gauge')
                for err in response_json['errors']:
                    metric.add_sample("locust_errors", value=err['occurrences'], labels={'path': err['name'], 'method': err['method'], 'error': err['error']})
                yield metric

                logger.info("report to promethues the current rps...")
                metric = Metric("rps", "Request per second", 'gauge')
                metric.add_sample("rps",
                                  value=response_json["stats"][len(response_json["stats"]) - 1]["current_rps"],
                                  labels={})
                yield metric


try:
    # Start up the server to expose the metrics.
    start_http_server(8000, registry=LocustCollector)
    print("start listening on port 8000...")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    exit(0)
