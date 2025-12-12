from diagrams import Diagram, Cluster
from diagrams.programming.framework import Flutter, FastAPI
from diagrams.onprem.database import MariaDB
from diagrams.generic.device import Mobile
from diagrams.onprem.container import Docker
from diagrams.programming.language import Python
from diagrams.aws.security import IAM

with Diagram("Bikeminer Architecture", show=False, direction="LR"):
    mobile = Mobile("Mobile Apps")
    
    with Cluster("Client Layer"):
        flutter = Flutter("Flutter App")
        auth = IAM("Authentication")
        
    with Cluster("Server Layer"):
        api = FastAPI("FastAPI Backend")
        db = MariaDB("MariaDB")
        
    with Cluster("Container Layer"):
        docker = Docker("Docker Container")
    
    mobile >> flutter >> auth >> api >> db
    api - docker
    db - docker