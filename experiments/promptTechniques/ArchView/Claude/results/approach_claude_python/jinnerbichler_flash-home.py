from diagrams import Diagram, Cluster
from diagrams.onprem.queue import RabbitMQ
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import MongoDB
from diagrams.onprem.monitoring import Grafana
from diagrams.programming.framework import Flask
from diagrams.onprem.network import HAProxy
from diagrams.onprem.compute import Server
from diagrams.onprem.inmemory import Redis

with Diagram("IOTA Flash Home Architecture", show=False, direction="TB"):
    with Cluster("Docker Environment"):
        mqtt = RabbitMQ("MQTT Broker")
        
        with Cluster("Home Assistant"):
            ha = Docker("Home Assistant")
            ha_config = Server("Config")
            ha_scripts = Server("Scripts")
            ha_custom = Server("Custom Components")
            
        with Cluster("Coffee Machine Client"):
            coffee = Flask("Coffee Client")
            coffee_config = Server("Config")
        
        with Cluster("Flash Servers"):
            flash_coffee = Docker("Coffee Flash Server")
            flash_provider = Docker("Provider Flash Server")
            mongo_coffee = MongoDB("Coffee MongoDB")
            mongo_provider = MongoDB("Provider MongoDB")
        
        with Cluster("IOTA Private Testnet"):
            iri = Docker("IRI Node")
            coordinator = Docker("Coordinator")
            spammer = Docker("Spammer")
            explorer = Docker("Explorer")
            
        with Cluster("Monitoring"):
            grafana = Grafana("Monitoring")
            cache = Redis("Cache")
            proxy = HAProxy("Load Balancer")

        # Define connections
        mqtt >> ha
        ha >> [ha_config, ha_scripts, ha_custom]
        ha >> coffee
        coffee >> coffee_config
        coffee >> [flash_coffee, flash_provider]
        flash_coffee >> mongo_coffee
        flash_provider >> mongo_provider
        [flash_coffee, flash_provider] >> iri
        iri >> [coordinator, spammer, explorer]
        [ha, coffee, flash_coffee, flash_provider, iri] >> proxy
        proxy >> grafana
        grafana >> cache