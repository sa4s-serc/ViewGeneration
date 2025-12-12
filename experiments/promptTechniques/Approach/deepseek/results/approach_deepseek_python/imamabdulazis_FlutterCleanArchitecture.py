from diagrams import Diagram, Cluster
from diagrams.generic.device import Mobile
from diagrams.onprem.client import User
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Celery
from diagrams.programming.framework import Flask
from diagrams.programming.language import Python

with Diagram("Flutter Clean Architecture", show=False, direction="TB"):
    user = User("User")
    
    with Cluster("Mobile App"):
        mobile = Mobile("Flutter App")
        presentation = Mobile("Presentation Layer\n(UI Components, BLoCs)")
    
    with Cluster("Backend Services"):
        nginx = Nginx("API Gateway")
        
        with Cluster("Application Layer"):
            flask = Flask("Flask App")
            celery = Celery("Celery Worker")
        
        with Cluster("Domain Layer"):
            python = Python("Business Logic\n(Use Cases, Entities)")
        
        with Cluster("Data Layer"):
            postgresql = PostgreSQL("PostgreSQL")
            redis = Redis("Redis Cache")
    
    user >> mobile
    mobile >> presentation
    presentation >> nginx
    nginx >> flask
    flask >> python
    python >> celery
    python >> postgresql
    python >> redis
    celery >> postgresql
    celery >> redis