from diagrams import Diagram, Cluster
from diagrams.aws.storage import S3
from diagrams.onprem.database import Postgresql
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.client import Users
from diagrams.onprem.network import Nginx
from diagrams.onprem.compute import Server
from diagrams.programming.language import Nodejs

with Diagram("Stock Management Application Architecture", show=False):
    user = Users("Client")

    with Cluster("Backend Services"):
        with Cluster("API Layer"):
            api_server = Nodejs("Node.js Express API")
        
        with Cluster("Business Logic"):
            controllers = Nodejs("API Controllers")
            middlewares = Nodejs("Middlewares")
        
        with Cluster("Data Access"):
            db_queries = Nodejs("Database Queries")
        
        with Cluster("Utility Functions"):
            utilities = Nodejs("Utilities")

        with Cluster("Configuration"):
            config = Nodejs("Configuration & Constants")
        
        with Cluster("Error Handling"):
            errors = Nodejs("Error Handling")

    with Cluster("Storage & Session Management"):
        database = Postgresql("Postgres DB")
        session_cache = Redis("Redis")
        image_storage = S3("AWS S3")

    user >> api_server >> controllers
    controllers >> middlewares
    middlewares >> db_queries
    db_queries >> database
    middlewares >> session_cache
    middlewares >> image_storage
    middlewares >> utilities
    middlewares >> config
    middlewares >> errors