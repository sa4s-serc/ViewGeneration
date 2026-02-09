from diagrams import Diagram, Cluster
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.container import Docker
from diagrams.onprem.queue import Celery, RabbitMQ
from diagrams.onprem.database import Postgresql
from diagrams.onprem.analytics import Hadoop, Spark, Hive
from diagrams.onprem.monitoring import Grafana
from diagrams.elastic.elasticsearch import Elasticsearch
from diagrams.elastic.elasticsearch import Kibana
from diagrams.onprem.network import Nginx
from diagrams.onprem.inmemory import Redis

with Diagram("Apache Airflow Architecture", show=False):
    with Cluster("Docker Environment"):
        docker = Docker("Docker")
        
        with Cluster("Airflow Core"):
            webserver = Nginx("Webserver")
            scheduler = Airflow("Scheduler")
            workers = [Airflow("Worker1"), Airflow("Worker2")]
            
        with Cluster("Message Brokers"):
            redis = Redis("Redis")
            rabbitmq = RabbitMQ("RabbitMQ")
            celery = Celery("Celery")
            
        with Cluster("Storage"):
            db = Postgresql("Metadata DB")
            
        with Cluster("Data Processing"):
            hadoop = Hadoop("HDFS")
            spark = Spark("Spark")
            hive = Hive("Hive")
            
        with Cluster("Monitoring"):
            grafana = Grafana("Grafana")
            elastic = Elasticsearch("Elasticsearch")
            kibana = Kibana("Kibana")

    # Core connections
    webserver >> db
    scheduler >> db
    for worker in workers:
        worker >> db
        worker >> redis
        worker >> celery
        
    # Data processing connections
    for worker in workers:
        worker >> hadoop
        worker >> spark
        worker >> hive
        
    # Monitoring connections
    webserver >> elastic
    scheduler >> elastic
    for worker in workers:
        worker >> elastic
    
    elastic >> kibana
    elastic >> grafana
    
    # Message broker connections
    celery >> rabbitmq
    celery >> redis