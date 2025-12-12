from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.programming.framework import Django
from diagrams.programming.framework import Angular
from diagrams.onprem.queue import RabbitMQ
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.database import PostgreSQL

with Diagram("Intelligent Bike System Architecture", show=False, direction="TB"):
    user = User("End User")
    
    with Cluster("Frontend Layer"):
        frontend = Angular("Angular Dashboard")
    
    with Cluster("Backend Layer"):
        with Cluster("API Server"):
            django = Django("Django REST API")
        
        with Cluster("Message Broker"):
            mqtt = RabbitMQ("MQTT Broker")
        
        with Cluster("Cache"):
            redis = Redis("Redis Cache")
    
    with Cluster("Data Layer"):
        with Cluster("Database"):
            db = PostgreSQL("PostgreSQL")
        
        with Cluster("File Storage"):
            storage = S3("File Storage")
    
    with Cluster("Hardware Layer"):
        with Cluster("Bike Sensors"):
            sensors = EC2("Sensor Hardware")
            lcd = Nginx("LCD Display")
    
    user >> frontend
    frontend >> django
    sensors >> mqtt
    mqtt >> django
    django >> redis
    django >> db
    django >> storage
    django >> lcd