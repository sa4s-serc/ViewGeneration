from diagrams import Diagram
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.queue import Celery, Rabbitmq
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.analytics import Spark, Hive
from diagrams.onprem.network import Nginx
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.compute import Server

with Diagram("Apache Airflow Architecture", show=False):
    nginx = Nginx("Nginx")
    
    airflow = Airflow("Airflow")
    scheduler = Server("Scheduler")
    webserver = Server("Web Server")
    worker = Celery("Worker")
    broker = Rabbitmq("Broker")
    result_backend = Redis("Result Backend")
    
    db = PostgreSQL("PostgreSQL")
    processing = Spark("Data Processing")
    storage = Hive("Data Storage")
    
    monitoring = Prometheus("Monitoring")
    dashboard = Grafana("Dashboard")
    
    nginx >> airflow
    airflow >> scheduler
    airflow >> webserver
    scheduler >> worker
    worker >> broker
    worker >> result_backend
    scheduler >> db
    worker >> processing
    processing >> storage
    monitoring >> dashboard