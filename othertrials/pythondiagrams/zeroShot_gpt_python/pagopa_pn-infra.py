from diagrams import Diagram, Cluster, Edge
from diagrams.generic.network import Subnet
from diagrams.onprem.compute import Server
from diagrams.onprem.database import MySQL
from diagrams.onprem.network import Nginx
from diagrams.onprem.client import User

with Diagram("System Architecture", show=True, direction="TB"):
    user = User("User")

    with Cluster("Web Tier"):
        nginx = Nginx("Nginx")
        web_server = Server("Web Server")

    with Cluster("Application Tier"):
        app_server = Server("Application Server")

    with Cluster("Data Tier"):
        db_master = MySQL("Primary DB")
        db_slave = MySQL("Replica DB")

    user >> Edge(label="HTTP Request", color="blue") >> nginx
    nginx >> Edge(label="Forward Request", color="black") >> web_server
    web_server >> Edge(label="API Call", color="green") >> app_server
    app_server >> Edge(label="Query", color="red") >> db_master

    db_master >> Edge(label="Replication", style="dashed", color="orange") >> db_slave