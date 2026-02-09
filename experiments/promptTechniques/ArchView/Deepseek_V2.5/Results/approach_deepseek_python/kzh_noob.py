from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.onprem.container import Docker
from diagrams.onprem.queue import RabbitMQ
from diagrams.onprem.database import MongoDB
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.tracing import Jaeger

with Diagram("Noob Code Execution Platform Architecture", show=False, direction="LR"):
    user = User("User")
    
    with Cluster("Kubernetes Cluster"):
        with Cluster("API Gateway"):
            ingress = Nginx("Nginx Ingress")
        
        with Cluster("Microservices"):
            with Cluster("Frontend"):
                frontend = Docker("Frontend Service")
            
            with Cluster("Auth Service"):
                auth = Docker("Auth Service")
            
            with Cluster("Problems Service"):
                problems = Docker("Problems Service")
            
            with Cluster("Submissions Service"):
                submissions = Docker("Submissions Service")
            
            with Cluster("Executor Service"):
                executor = Docker("Executor Service")
        
        with Cluster("Message Queue"):
            rabbitmq = RabbitMQ("RabbitMQ")
        
        with Cluster("Data Layer"):
            with Cluster("Databases"):
                mongodb = MongoDB("MongoDB")
                redis = Redis("Redis")
            
            with Cluster("Tracing"):
                jaeger = Jaeger("Jaeger")

    user >> ingress
    ingress >> frontend
    ingress >> auth
    ingress >> problems
    ingress >> submissions
    
    submissions >> rabbitmq
    rabbitmq >> executor
    
    auth >> redis
    problems >> mongodb
    submissions >> mongodb
    executor >> mongodb
    
    frontend >> jaeger
    auth >> jaeger
    problems >> jaeger
    submissions >> jaeger
    executor >> jaeger