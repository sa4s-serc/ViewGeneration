from diagrams import Diagram, Cluster, Edge
from diagrams.generic.database import SQL
from diagrams.generic.compute import Rack
from diagrams.onprem.network import Nginx
from diagrams.onprem.client import Client
from diagrams.programming.language import Python
from diagrams.onprem.iac import Ansible
from diagrams.onprem.queue import Rabbitmq
from diagrams.onprem.container import Docker

with Diagram("MyEMS Architecture", show=False, direction="TB"):
    client = Client("User Interface")

    with Cluster("MyEMS System"):
        with Cluster("Microservices-like Architecture"):
            api_service = Python("Falcon RESTful API")
            modbus_service = Python("Modbus TCP Service")
            aggregation_service = Python("Aggregation Service")
            normalization_service = Python("Normalization Service")

        with Cluster("Database Layer"):
            system_db = SQL("System DB")
            energy_db = SQL("Energy DB")
            billing_db = SQL("Billing DB")
            historical_db = SQL("Historical DB")
            carbon_db = SQL("Carbon DB")

        api_service >> Edge(label="CRUD Operations") >> system_db
        api_service >> Edge(label="Data Access") >> energy_db
        api_service >> Edge(label="Billing Access") >> billing_db
        api_service >> Edge(label="Historical Data") >> historical_db
        api_service >> Edge(label="Carbon Data") >> carbon_db

        modbus_service >> Edge(label="Data Acquisition") >> api_service
        aggregation_service >> Edge(label="Data Aggregation") >> api_service
        normalization_service >> Edge(label="Data Normalization") >> api_service

    client >> Edge(label="Access via API") >> api_service

    with Cluster("Infrastructure"):
        nginx = Nginx("Load Balancer")
        rabbitmq = Rabbitmq("Message Queue")
        docker = Docker("Containerization Platform")
        ansible = Ansible("Configuration Management")

    api_service >> Edge(label="Through Load Balancer") >> nginx
    api_service >> Edge(label="Message Queue") >> rabbitmq
    docker << Edge(label="Deployment") << api_service
    ansible << Edge(label="Configuration") << docker