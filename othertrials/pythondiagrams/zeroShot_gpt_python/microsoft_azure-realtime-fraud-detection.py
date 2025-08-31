from diagrams import Diagram, Cluster, Edge
from diagrams.generic.network import Firewall
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Internet
from diagrams.onprem.queue import RabbitMQ
from diagrams.programming.language import Python

with Diagram("Architectural View", show=False, direction="TB"):
    user = User("User")
    internet = Internet("Internet")

    with Cluster("System"):
        with Cluster("Microservices Layer"):
            service1 = Server("Service 1")
            service2 = Server("Service 2")
            service3 = Server("Service 3")

        with Cluster("Database Layer"):
            db_master = PostgreSQL("Master DB")
            db_slave = PostgreSQL("Slave DB")

        with Cluster("Message Queue"):
            queue = RabbitMQ("RabbitMQ")

    user >> Edge(label="HTTP Request", color="blue") >> internet >> Edge(label="API Call", color="blue") >> service1
    service1 >> Edge(label="REST API", color="green") >> service2
    service2 >> Edge(label="Function Call", color="green") >> service3
    service3 >> Edge(label="DB Query", color="red") >> db_master
    db_master >> Edge(label="Replication", color="red", style="dotted") >> db_slave
    service1 >> Edge(label="Message", color="purple") >> queue
    queue >> Edge(label="Message", color="purple") >> service3