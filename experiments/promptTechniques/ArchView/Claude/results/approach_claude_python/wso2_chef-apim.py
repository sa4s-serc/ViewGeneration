from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.network import Apache
from diagrams.onprem.database import MySQL
from diagrams.onprem.compute import Server
from diagrams.onprem.queue import RabbitMQ
from diagrams.onprem.container import Docker
from diagrams.generic.blank import Blank

with Diagram("WSO2 API Manager Chef Cookbook Architecture", show=False):
    with Cluster("WSO2 API Manager Deployment"):
        chef = Blank("Chef Cookbook")
        
        with Cluster("Infrastructure Components"):
            docker = Docker("Container Runtime")
            server = Server("Host Server")
            db = MySQL("MySQL Database")
            mq = RabbitMQ("Message Queue")
            web = Apache("Web Server")

            with Cluster("Deployment Profiles"):
                profiles = [
                    Server("Key Manager"),
                    Server("Publisher"),
                    Server("Store"),
                    Server("Traffic Manager"),
                    Server("Gateway")
                ]

        # Configuration Management Flow
        chef >> Edge(label="configures") >> docker
        chef >> Edge(label="manages") >> server
        chef >> Edge(label="configures") >> db
        chef >> Edge(label="configures") >> mq
        chef >> Edge(label="configures") >> web

        # Component Dependencies
        docker - server 
        server - db
        server - mq
        server - web

        # Profile Dependencies
        for profile in profiles:
            server >> profile
            db << profile
            mq << profile

        # Data Flow
        db << mq
        web >> db