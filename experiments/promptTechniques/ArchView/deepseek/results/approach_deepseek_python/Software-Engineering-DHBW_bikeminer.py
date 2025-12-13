from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.generic.os import Android
from diagrams.programming.framework import Flutter
from diagrams.programming.framework import FastAPI
from diagrams.onprem.database import MariaDB
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Internet

with Diagram("Bikeminer Architecture", show=False, direction="TB"):
    user = User("Cyclist")
    
    with Cluster("Mobile Clients"):
        android = Android("Legacy Android App")
        flutter = Flutter("Flutter App")
        mobile_clients = [android, flutter]
    
    internet = Internet("Internet")
    
    with Cluster("Backend Services"):
        with Cluster("Docker Container"):
            api = FastAPI("FastAPI Backend")
            db = MariaDB("MariaDB")
            api >> db
    
    user >> mobile_clients
    mobile_clients >> internet
    internet >> api