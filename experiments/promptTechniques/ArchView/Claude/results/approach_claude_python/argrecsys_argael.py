from diagrams import Diagram, Cluster
from diagrams.onprem.compute import Server
from diagrams.onprem.database import MySQL
from diagrams.programming.language import Java
from diagrams.onprem.client import Users
from diagrams.onprem.database import Oracle
from diagrams.programming.framework import Spring
from diagrams.onprem.queue import Kafka

with Diagram("ARGAEL Architecture", show=False):
    with Cluster("User Interface Layer"):
        users = Users("Users")
        gui = Java("ArgaelForm GUI")

    with Cluster("Application Layer"):
        app = Spring("ARGAEL Application")
        report = Server("Report Generator")

    with Cluster("Data Layer"):
        with Cluster("Storage"):
            mysql = MySQL("Users & Config")
            oracle = Oracle("Proposals & Comments")
        
        queue = Kafka("Event Queue")

    # Connect components
    users >> gui
    gui >> app
    app >> report
    app >> mysql
    app >> oracle
    app >> queue
    queue >> report

    report >> oracle