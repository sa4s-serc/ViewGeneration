from diagrams import Diagram
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.programming.framework import Spring
from diagrams.onprem.database import Postgresql
from diagrams.onprem.inmemory import Redis

with Diagram("Member Invitation System Architecture", show=False, direction="TB"):
    user = User("Workspace Manager")
    
    api_gateway = Nginx("API Gateway")
    
    interface_layer = Spring("Interface Layer\n(REST Controllers)")
    
    domain_layer = Spring("Domain Layer\n(Services & Use Cases)")
    
    redis_adapter = Spring("Redis Adapter\n(Invitation Storage)")
    database_adapter = Spring("Database Adapter\n(Member Storage)")
    
    redis = Redis("Redis\n(Invitation Cache)")
    database = Postgresql("Relational Database\n(Member Data)")
    
    user >> api_gateway
    api_gateway >> interface_layer
    interface_layer >> domain_layer
    domain_layer >> redis_adapter
    domain_layer >> database_adapter
    redis_adapter >> redis
    database_adapter >> database