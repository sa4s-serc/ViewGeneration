from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.database import PostgreSQL
from diagrams.programming.framework import Angular, DotNet
from diagrams.onprem.network import Nginx
from diagrams.onprem.container import Docker
from diagrams.aws.security import IAM

with Diagram("Contact Management System Architecture", show=False):
    with Cluster("Docker Environment"):
        load_balancer = Nginx("NGINX Load Balancer")
        
        with Cluster("Frontend"):
            frontend = Angular("Angular Frontend\nSSR Enabled")
        
        with Cluster("Backend"):
            api = DotNet(".NET Core API\nClean Architecture")
        
        with Cluster("Database"):
            db = PostgreSQL("PostgreSQL")

        docker = Docker("Docker\nContainer")
        auth = IAM("JWT Auth")
        
        # Define relationships
        load_balancer >> frontend
        load_balancer >> api
        
        frontend >> api
        api >> auth
        api >> db
        
        # Docker containerization
        docker >> load_balancer
        docker >> frontend
        docker >> api
        docker >> db