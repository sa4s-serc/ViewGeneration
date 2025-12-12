from diagrams import Diagram, Cluster
from diagrams.aws.compute import ECS
from diagrams.azure.identity import ActiveDirectory
from diagrams.programming.framework import FastAPI
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.firebase.develop import Authentication
from diagrams.onprem.client import Users
from diagrams.azure.web import APIConnections

with Diagram("CoolStore Microservices Architecture", show=False):
    with Cluster("Frontend"):
        users = Users("Customers")
        webui = APIConnections("Blazor WebUI")

    with Cluster("Identity & Auth"):
        identity = ActiveDirectory("IdentityServer4")
        auth = Authentication("Authentication")

    with Cluster("Backend Services"):
        with Cluster("Product Catalog Service"):
            product_api = FastAPI("Product API")
            product_db = PostgreSQL("Product DB")
            product_cache = Redis("Cache")
            
        with Cluster("Inventory Service"):
            inventory_api = FastAPI("Inventory API")
            inventory_db = PostgreSQL("Inventory DB")

    users >> webui
    webui >> identity
    webui >> product_api
    webui >> inventory_api
    
    product_api >> product_db
    product_api >> product_cache
    
    inventory_api >> inventory_db
    
    product_api >> auth
    inventory_api >> auth
    identity >> auth