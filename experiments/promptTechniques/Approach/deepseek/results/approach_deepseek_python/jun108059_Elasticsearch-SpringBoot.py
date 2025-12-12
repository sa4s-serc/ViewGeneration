from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3
from diagrams.onprem.client import User
from diagrams.onprem.database import MySQL
from diagrams.elastic.elasticsearch import Elasticsearch
from diagrams.programming.framework import Spring

with Diagram("Spring Boot Elasticsearch Application Architecture", show=False, direction="TB"):
    user = User("End User")
    
    with Diagram("Web Layer"):
        lb = ELB("Load Balancer")
        app_instances = [Spring("Spring Boot App") for _ in range(2)]
        
    with Diagram("Data Layer"):
        mysql = MySQL("MySQL Database")
        es = Elasticsearch("Elasticsearch Cluster")
        s3 = S3("Backup Storage")
    
    user >> lb >> app_instances
    app_instances >> mysql
    app_instances >> es
    mysql >> s3