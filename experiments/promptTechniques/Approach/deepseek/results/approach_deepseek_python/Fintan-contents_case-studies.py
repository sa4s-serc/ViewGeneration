from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3
from diagrams.onprem.client import User

with Diagram("Fintan Case Studies Architecture", show=False):
    with Cluster("Frontend"):
        user = User("End User")
        react_app = EC2("React App")
        mobile_app = EC2("Mobile App")
    
    with Cluster("Backend Services"):
        with Cluster("API Layer"):
            spring_boot = EC2("Spring Boot API")
        
        with Cluster("Data Layer"):
            database = RDS("PostgreSQL")
            cache = EC2("Redis Cache")
        
        with Cluster("Message Queue"):
            zeromq = EC2("ZeroMQ")
    
    with Cluster("CI/CD Pipeline"):
        ci_cd = EC2("Azure DevOps")
    
    with Cluster("Monitoring"):
        monitoring = EC2("New Relic")
        logging = EC2("Elastic Stack")
    
    user >> react_app
    user >> mobile_app
    react_app >> spring_boot
    mobile_app >> spring_boot
    spring_boot >> database
    spring_boot >> cache
    spring_boot >> zeromq
    ci_cd >> spring_boot
    spring_boot >> monitoring
    spring_boot >> logging