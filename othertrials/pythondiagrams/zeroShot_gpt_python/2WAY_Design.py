from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.custom import Custom

with Diagram("Sample Architecture", show=True, direction="LR"):
    with Cluster("Client Layer"):
        client = Custom("Client", "./icons/client.png")
    
    with Cluster("Load Balancer"):
        lb = ELB("Load Balancer")
    
    with Cluster("Application Layer"):
        services = [EC2("Service 1"),
                    EC2("Service 2"),
                    EC2("Service 3")]
    
    with Cluster("Database Layer"):
        db_primary = RDS("Primary DB")
        db_replica = RDS("Replica DB")
    
    client >> lb >> services
    services >> Edge(label="read/write") >> db_primary
    db_primary >> Edge(style="dashed", label="replication") >> db_replica