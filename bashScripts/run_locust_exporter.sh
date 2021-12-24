#!/bin/bash
docker run --net=host --rm containersol/locust_exporter --locust.uri=http://192.168.2.109:4200 --web.listen-address=192.168.2.110:9646