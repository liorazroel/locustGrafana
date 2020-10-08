This is a load testing project using locustio library, for more information - https://locust.io/ <br />
1.add .env file with your environment variable:TOKEN, ORG, BUCKET - for influxDATA cloud <br />
for more information - https://www.influxdata.com/products/influxdb-cloud/ <br /> 
2.install promethues client from the site - https://prometheus.io/download/<br />
3.visualize the data of promethues and influxData in grafana - you can import my dashboard_grafana.json file to grafana or create your grafana dashboard<br />
4.run the locust command - locust --web-host=localhost -f locustfiles/locustfileCloud.py <br />
5.run the promethues server after running the locust command - you can stay this server run always in the background


![image](https://user-images.githubusercontent.com/52318755/95489103-11eb1080-099f-11eb-938e-cfb87019adec.jpeg)

enjoy :)

credit to: https://github.com/mbolek/locust_exporter
