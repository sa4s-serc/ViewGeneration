from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.programming.framework import Angular
from diagrams.onprem.database import Postgresql
from diagrams.aws.compute import EC2

with Diagram("Contact Management Application Architecture", show=False, direction="LR"):
    user = User("End User")
    
    with Cluster("Frontend"):
        frontend = Angular("Angular App")
    
    with Cluster("Load Balancer"):
        load_balancer = Nginx("Nginx")
    
    with Cluster("Backend Services"):
        with Cluster(".NET Core API"):
            api = EC2("Web API")
            application = EC2("Application Layer")
            domain = EC2("Domain Layer")
            infrastructure = EC2("Infrastructure Layer")
        
        with Cluster("Database"):
            database = Postgresql("PostgreSQL")
    
    user >> load_balancer
    load_balancer >> frontend
    frontend >> api
    api >> application
    application >> domain
    domain >> infrastructure
    infrastructure >> database