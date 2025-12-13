from diagrams import Diagram, Cluster, Edge
from diagrams.programming.framework import Spring
from diagrams.programming.framework import Angular
from diagrams.onprem.client import Client
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker
from diagrams.generic.storage import Storage
from diagrams.generic.database import SQL
from diagrams.onprem.iac import Terraform
from diagrams.generic.network import Firewall

with Diagram("LwM2M and Blockchain System Architecture", show=False, direction="TB"):
    angular_app = Angular("Anomaly Detection App")

    with Cluster("MainApp"):
        backend = Spring("Spring Boot Backend")
        with Cluster("REST API Controllers"):
            client_controller = Docker("ClientController")
            anomaly_controller = Docker("AnomalyController")
            login_controller = Docker("LoginController")
            user_controller = Docker("UserController")

        with Cluster("Services"):
            client_service = Docker("ClientService")
            anomaly_service = Docker("AnomalyService")
            user_service = Docker("UserService")
            blockchain_service = Docker("BlockchainService")

        with Cluster("Smart Contracts"):
            user_store = Terraform("UserStore")
            client_store = Terraform("ClientStore")
            anomaly_store = Terraform("AnomalyStore")

        blockchain = Server("Ethereum Blockchain")

    with Cluster("LwM2M Components"):
        lwm2m_server = Client("LwM2M Server")
        bootstrap_server = Client("Bootstrap Server")
        lwm2m_client = Client("LwM2M Client")

    storage = Storage("Anomaly Data Store")

    angular_app >> Edge(label="Fetch Client Data") >> client_service
    angular_app >> Edge(label="Report Anomalies") >> anomaly_service
    angular_app >> Edge(label="User Authentication") >> login_controller

    client_service >> Edge(label="Manage Clients") >> client_controller
    anomaly_service >> Edge(label="Handle Anomalies") >> anomaly_controller
    user_service >> Edge(label="User Management") >> user_controller

    blockchain_service >> Edge(label="Interact with Smart Contracts") >> blockchain
    blockchain >> Edge(label="Store Anomalies") >> anomaly_store
    blockchain >> Edge(label="Manage Users") >> user_store
    blockchain >> Edge(label="Manage Clients") >> client_store

    lwm2m_server >> Edge(label="Monitor Environment") >> bootstrap_server
    lwm2m_server >> Edge(label="Secure Communication") >> client_store
    bootstrap_server >> Edge(label="Retrieve Security Info") >> blockchain

    lwm2m_client >> Edge(label="Simulate IoT Device") >> lwm2m_server

    anomaly_service >> Edge(label="Store Data") >> storage