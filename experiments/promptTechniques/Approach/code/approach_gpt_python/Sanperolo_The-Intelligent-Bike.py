from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.iac import Terraform
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka
from diagrams.onprem.database import PostgreSQL
from diagrams.programming.framework import Django
from diagrams.programming.language import Python
from diagrams.programming.language import NodeJS

with Diagram("The Intelligent Bike Architecture", show=False, direction="LR"):

    user = User("User")

    with Cluster("Hardware Interface"):
        sensors = [
            Python("Velocity Sensor"),
            Python("Humidity Sensor"),
            Python("Temperature Sensor"),
            Python("GPS Sensor"),
            Python("Gyroscope"),
            Python("Light Sensor"),
            Python("Rain Sensor")
        ]
        mqtt_client = Kafka("MQTT Broker")
        lcd_display = Python("LCD Display")
        leds = Python("LED Control")

    with Cluster("Backend"):
        django_api = Django("Django REST API")
        mqtt_handler = Python("MQTT Handler")
        db_dev = PostgreSQL("SQLite (Dev)")
        db_prod = PostgreSQL("PostgreSQL (Prod)")

    with Cluster("Frontend"):
        angular_app = NodeJS("Angular App")
        web_server = Nginx("Web Server")

    user >> Edge(label="Web Interface") >> web_server >> angular_app
    angular_app >> Edge(label="REST API Calls") >> django_api
    django_api >> Edge(label="Data Storage") >> [db_dev, db_prod]
    django_api << Edge(label="Data Ingestion") << mqtt_handler
    mqtt_client >> Edge(label="Sensor Data") >> mqtt_handler
    mqtt_client << Edge(label="Publish Data") << sensors
    mqtt_client >> Edge(label="Control Commands") >> [lcd_display, leds]