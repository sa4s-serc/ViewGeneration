from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.programming.language import Python
from diagrams.programming.framework import FastAPI

with Diagram("Architecture Overview", show=False):
    user = User("User")
    
    with Cluster("Frontend"):
        frontend = Nginx("Web Server")
    
    with Cluster("Backend"):
        api = FastAPI("API")
        app_logic = Python("Application Logic")
        
        with Cluster("Database"):
            db_primary = PostgreSQL("Primary DB")
            db_replica = PostgreSQL("Replica DB")
            cache = Redis("Cache")
    
    with Cluster("Storage"):
        storage = S3("Object Storage")
    
    user >> frontend >> api >> app_logic
    app_logic >> db_primary
    app_logic >> db_replica
    app_logic >> cache
    app_logic >> storage