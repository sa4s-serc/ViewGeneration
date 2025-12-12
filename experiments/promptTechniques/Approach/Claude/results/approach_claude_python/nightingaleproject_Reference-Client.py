from diagrams import Diagram, Cluster
from diagrams.programming.framework import React, DotNet
from diagrams.onprem.database import PostgreSQL
from diagrams.azure.web import APIConnections
from diagrams.firebase.develop import Authentication
from diagrams.programming.language import Javascript
from diagrams.onprem.queue import RabbitMQ

with Diagram("Nightingale Project Reference Client Architecture", show=False, direction="TB"):
    with Cluster("Frontend"):
        ui = React("React UI")
        js = Javascript("Client Logic")

    with Cluster("Backend Services"):
        api = APIConnections("API Controllers")
        auth = Authentication("Authentication")
        dotnet = DotNet(".NET Core")
        queue = RabbitMQ("Message Queue")
        db = PostgreSQL("PostgreSQL")

    ui >> js >> api
    api >> auth
    api >> dotnet
    dotnet >> queue
    dotnet >> db
    queue >> dotnet