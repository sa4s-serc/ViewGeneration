from diagrams import Diagram
from diagrams.generic.os import LinuxGeneral
from diagrams.programming.language import Python
from diagrams.programming.framework import React, Flask, Django
from diagrams.onprem.database import PostgreSQL, MongoDB
from diagrams.onprem.queue import RabbitMQ
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.network import Nginx
from diagrams.onprem.container import Docker
from diagrams.onprem.ci import Jenkins

with Diagram("Software Architecture View", show=False, direction="TB"):
    client = LinuxGeneral("Client")
    
    with Diagram("Frontend Layer"):
        react_app = React("React App")
        nginx = Nginx("Nginx")
        
    with Diagram("Backend Layer"):
        flask_api = Flask("Flask API")
        django_app = Django("Django App")
        
    with Diagram("Data Layer"):
        postgres = PostgreSQL("PostgreSQL")
        mongodb = MongoDB("MongoDB")
        rabbitmq = RabbitMQ("Message Queue")
        
    with Diagram("Infrastructure Layer"):
        docker = Docker("Container Runtime")
        jenkins = Jenkins("CI/CD")
        grafana = Grafana("Monitoring")
        prometheus = Prometheus("Metrics")
    
    client >> nginx >> [flask_api, django_app]
    flask_api >> [postgres, rabbitmq]
    django_app >> [mongodb, rabbitmq]
    rabbitmq >> flask_api
    [flask_api, django_app] >> prometheus
    prometheus >> grafana
    jenkins >> docker