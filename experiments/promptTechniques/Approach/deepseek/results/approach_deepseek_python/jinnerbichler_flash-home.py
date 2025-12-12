from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker
from diagrams.onprem.database import MongoDB
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Internet
from diagrams.programming.language import Python, Nodejs
from diagrams.aws.iot import IotMqtt

with Diagram("IOTA Flash Home Automation Architecture", show=False, direction="TB"):
    user = User("Home Assistant User")
    
    with Cluster("Home Automation System"):
        home_assistant = Server("Home Assistant")
        mqtt_broker = IotMqtt("MQTT Broker")
        
        with Cluster("Coffee Machine System"):
            coffee_client = Python("Coffee Machine Client")
            coffee_machine = Server("Smart Coffee Machine")
    
    with Cluster("IOTA Flash System"):
        with Cluster("Flash Servers"):
            coffee_flash_server = Nodejs("Coffee Machine Flash Server")
            provider_flash_server = Nodejs("Provider Flash Server")
        
        with Cluster("IOTA Network"):
            iota_node = Server("IOTA IRI Node")
            coordinator = Server("Coordinator")
            explorer = Server("Explorer")
    
    with Cluster("Data Storage"):
        mongo_coffee = MongoDB("Coffee MongoDB")
        mongo_provider = MongoDB("Provider MongoDB")
    
    user >> home_assistant
    home_assistant >> mqtt_broker
    mqtt_broker >> coffee_client
    coffee_client >> coffee_machine
    coffee_client >> coffee_flash_server
    coffee_flash_server >> provider_flash_server
    coffee_flash_server >> iota_node
    provider_flash_server >> iota_node
    iota_node >> coordinator
    iota_node >> explorer
    coffee_flash_server >> mongo_coffee
    provider_flash_server >> mongo_provider
    internet = Internet("Internet")
    home_assistant >> internet
    coffee_flash_server >> internet
    provider_flash_server >> internet