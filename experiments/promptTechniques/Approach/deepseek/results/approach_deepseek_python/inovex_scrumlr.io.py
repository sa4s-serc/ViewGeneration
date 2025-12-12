from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.queue import Nats
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.container import Docker
from diagrams.programming.framework import React
from diagrams.programming.language import Go

with Diagram("Scrumlr.io Architecture", show=False, direction="TB"):
    user = User("User")

    with Cluster("Frontend"):
        frontend = React("React App")
        redux = React("Redux Store")

    with Cluster("Backend"):
        with Cluster("API Layer"):
            api = Go("API Handlers")
            router = Go("Router")
            middleware = Go("Middleware")

        with Cluster("Business Logic"):
            services = Go("Services")
            auth = Go("Authentication")

        with Cluster("Data Access"):
            database = PostgreSQL("PostgreSQL")
            orm = Go("ORM Layer")

    with Cluster("Real-time Communication"):
        websockets = Nats("WebSockets")
        nats = Nats("NATS")
        redis = Redis("Redis")

    with Cluster("Infrastructure"):
        docker = Docker("Docker")
        compose = Docker("Docker Compose")

    user >> frontend
    frontend >> redux
    frontend >> api
    api >> router
    router >> middleware
    middleware >> services
    services >> auth
    services >> orm
    orm >> database
    api >> websockets
    websockets >> nats
    nats >> redis
    docker >> compose