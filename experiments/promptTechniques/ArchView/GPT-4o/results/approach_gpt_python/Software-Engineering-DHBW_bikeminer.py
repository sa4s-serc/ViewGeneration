from diagrams import Diagram, Cluster
from diagrams.programming.framework import Flutter
from diagrams.programming.language import Python
from diagrams.onprem.client import Client
from diagrams.onprem.database import MariaDB
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Internet
from diagrams.generic.os import Android
from diagrams.generic.device import Mobile

with Diagram("Bikeminer Project Architecture", show=False, direction="TB"):
    with Cluster("Client Tier"):
        android_app = Android("Android App (Legacy)")
        flutter_app = Flutter("Flutter App")

    with Cluster("Backend Tier"):
        with Cluster("Containerized Environment"):
            api_container = Docker("FastAPI Backend")
            db_container = Docker("MariaDB Database")

        with Cluster("FastAPI Application"):
            api = Python("FastAPI")

    with Cluster("Data Storage"):
        database = MariaDB("MariaDB")

    client = Client("User")

    client >> android_app
    client >> flutter_app

    android_app >> Internet("REST API") >> api
    flutter_app >> Internet("REST API") >> api

    api >> database
    database << db_container

    api_container >> api
    api_container << db_container