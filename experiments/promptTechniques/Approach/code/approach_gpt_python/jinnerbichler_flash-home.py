from diagrams import Diagram, Cluster, Node
from diagrams.custom import Custom
from diagrams.onprem.client import Client
from diagrams.onprem.network import Nginx
from diagrams.onprem.iac import Ansible
from diagrams.programming.language import Python
from diagrams.onprem.container import Docker
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.compute import Server
from diagrams.onprem.queue import RabbitMQ
from diagrams.onprem.database import Mongodb

with Diagram("Smart Coffee Machine Architecture", show=False, direction="TB"):
    with Cluster("Smart Coffee System"):
        home_assistant = Custom("Home Assistant", "./icons/home_assistant.png")
        
        with Cluster("Coffee Machine Client"):
            coffee_client = Python("Coffee Client")
            coffee_client_config = Custom("Config", "./icons/config.png")
        
        with Cluster("Flash Servers"):
            coffee_flash_server = Node("Coffee Flash Server")
            provider_flash_server = Node("Provider Flash Server")
        
        private_iota_testnet = Nginx("Private IOTA Testnet")
    
    home_assistant >> RabbitMQ("MQTT") >> coffee_client
    home_assistant >> coffee_flash_server
    coffee_client >> coffee_flash_server
    coffee_flash_server >> provider_flash_server
    provider_flash_server >> private_iota_testnet
    coffee_flash_server >> private_iota_testnet
    
    with Cluster("Dockerized Environment"):
        docker_compose = Docker("Docker Compose")
        ansible = Ansible("Fabric Deployment")
        
    docker_compose >> [home_assistant, coffee_client, coffee_flash_server, provider_flash_server, private_iota_testnet]
    ansible >> docker_compose

    mongo_db = Mongodb("MongoDB Instances")
    grafana = Grafana("Monitoring")
    
    docker_compose >> mongo_db
    docker_compose >> grafana