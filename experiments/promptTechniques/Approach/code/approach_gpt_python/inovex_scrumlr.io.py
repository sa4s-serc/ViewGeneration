from diagrams import Diagram, Cluster
from diagrams.aws.general import User
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.queue import Nats
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Nginx
from diagrams.onprem.network import Envoy
from diagrams.programming.framework import React
from diagrams.programming.language import Go

with Diagram("Scrumlr.io Architecture", show=False, direction="TB"):
    with Cluster("Frontend"):
        client = User("Client")
        react_app = React("React App")

    with Cluster("Backend"):
        go_app = Go("Go Server")
        nginx = Nginx("Nginx")
        envoy = Envoy("Envoy")

        client >> nginx >> envoy >> go_app

        with Cluster("Real-time Communication"):
            nats = Nats("NATS")
            redis = Redis("Redis")

        go_app >> nats
        go_app >> redis

    with Cluster("Database"):
        db = PostgreSQL("PostgreSQL")

    go_app >> db

    client >> react_app
    react_app >> nginx