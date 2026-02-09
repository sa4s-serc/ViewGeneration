from diagrams import Diagram, Cluster
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Nginx
from diagrams.onprem.compute import Server
from diagrams.programming.framework import Angular, Django 
from diagrams.onprem.queue import RabbitMQ
from diagrams.generic.compute import Rack

with Diagram("The Intelligent Bike Architecture", show=False):
    with Cluster("Hardware Layer"):
        sensors = Rack("Bike Sensors")
        lcd = Rack("LCD Display")

    with Cluster("Communication Layer"):
        mqtt = RabbitMQ("MQTT Broker")

    with Cluster("Backend Layer"):
        with Cluster("API Server"):
            api = Django("Django REST API")
            db = PostgreSQL("PostgreSQL")
            api >> db

    with Cluster("Frontend Layer"):
        with Cluster("Web Application"):
            web_server = Nginx("Web Server")
            frontend = Angular("Dashboard UI")
            web_server >> frontend

    # Define the data flow
    sensors >> mqtt >> api
    api >> web_server
    lcd << mqtt