from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Internet
from diagrams.onprem.container import Docker
from diagrams.programming.framework import React
from diagrams.programming.language import Csharp

with Diagram("Nightingale Project Reference Client Architecture", show=False):
    internet = Internet("NVSS API Server")

    with Cluster("Nightingale Client"):
        user = User("Jurisdiction User")
        ui = React("React UI")

        with Cluster("Backend Services"):
            backend = Csharp("ASP.NET Core")
            timed_service = Csharp("TimedHostedService")

        with Cluster("Database"):
            db = PostgreSQL("PostgreSQL")

        user >> ui >> Edge(label="REST API") >> backend
        backend >> Edge(label="Database Access") >> db
        backend >> Edge(label="API Interaction") >> internet
        timed_service >> Edge(label="Polling & Message Handling") >> backend

    with Cluster("Development Environment"):
        Docker("Docker Container") - Edge(label="Includes") - db

    user >> Edge(label="UI Interaction") >> ui