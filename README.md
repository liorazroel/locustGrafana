This is a load testing project using locustio library, for more information - https://locust.io/ <br />
<h2>prerequisites</h2> <br />
1. Promethues server web UI  <br />
2. Grafana Web UI <br />
3. docker on machine <br /><br />

<h2> Instructions </h2> <br />
1. On linux machine run this command in order to install the exporter - cd bashScripts & ./run_locust_exporter.sh <br />
2. On promethues copy the job config which name is locust_exporter see in promethues.yml 
3. Run the loucst script you want.
4. On grafana add datasource promethues
5. Import dashboard_grafana.json from this project


![grafana_image](https://grafana.com/api/dashboards/11985/images/7794/image)

enjoy :)