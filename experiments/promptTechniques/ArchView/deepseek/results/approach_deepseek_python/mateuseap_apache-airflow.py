from diagrams import Diagram, Cluster
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.database import Postgresql
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.analytics import Spark, Hadoop
from diagrams.onprem.queue import Celery
from diagrams.onprem.container import Docker
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.logging import Elasticsearch, Logstash, Kibana
from diagrams.onprem.network import Nginx
from diagrams.programming.language import Python
from diagrams.generic.os import Linux

with Diagram("Apache Airflow Learning Repository Architecture", show=False, direction="TB"):
    with Cluster("Docker Environment"):
        docker = Docker("Docker")
        
        with Cluster("Airflow Core"):
            scheduler = Airflow("Scheduler")
            webserver = Airflow("Web Server")
            worker = Airflow("Worker")
            
        with Cluster("Database"):
            postgres = Postgresql("PostgreSQL")
            
        with Cluster("Message Broker"):
            redis = Redis("Redis")
            
        with Cluster("Monitoring"):
            grafana = Grafana("Grafana")
            prometheus = Prometheus("Prometheus")
            
        with Cluster("Logging"):
            elasticsearch = Elasticsearch("Elasticsearch")
            logstash = Logstash("Logstash")
            kibana = Kibana("Kibana")
            
    with Cluster("Hadoop Ecosystem"):
        hadoop = Hadoop("Hadoop")
        spark = Spark("Spark")
        
    with Cluster("External Services"):
        http = Nginx("HTTP Source")
        email = Linux("Email")
        slack = Linux("Slack")
        
    with Cluster("DAGs"):
        dag_python = Python("Python DAGs")
        dag_scripts = Python("Processing Scripts")
        
    docker >> [scheduler, webserver, worker]
    scheduler >> postgres
    scheduler >> redis
    worker >> redis
    webserver >> postgres
    
    scheduler >> [grafana, prometheus]
    worker >> [grafana, prometheus]
    webserver >> [grafana, prometheus]
    
    scheduler >> elasticsearch
    worker >> elasticsearch
    webserver >> elasticsearch
    
    worker >> hadoop
    worker >> spark
    
    worker >> http
    worker >> email
    worker >> slack
    
    dag_python >> worker
    dag_scripts >> worker