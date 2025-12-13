from diagrams import Diagram, Cluster, Edge
from diagrams.programming.framework import React
from diagrams.onprem.client import Users
from diagrams.onprem.compute import Server
from diagrams.onprem.database import Mongodb
from diagrams.onprem.network import Nginx
from diagrams.onprem.container import Docker
from diagrams.generic.os import Windows

with Diagram("HypnoLog Architecture", show=False, direction="LR"):
    users = Users("Developers")

    with Cluster("HypnoLog System"):
        server = Server("Node.js/Express")
        socketio = Server("Socket.IO")
        ajv = Server("Ajv")
        
        with Cluster("Web UI"):
            client = React("HTML/JavaScript/CSS")
            systemjs = React("SystemJS")
            jquery = React("JQuery")
            visualizers = React("Visualizers")
            windows = React("Windows")
            config_factory = React("ConfigFactory")
            windows_dispatcher = React("WindowsDispatcher")
            windows_filter = React("WindowsFilter")

        client >> Edge(label="loads modules") >> systemjs
        client >> Edge(label="DOM manipulation") >> jquery
        client >> Edge(label="visualize data") >> visualizers
        client >> Edge(label="manage & arrange") >> windows
        client >> Edge(label="config management") >> config_factory

        visualizers << Edge(label="dispatch data") >> windows_dispatcher
        windows_dispatcher >> windows
        windows_filter << Edge(label="filter by tags") >> windows

        server >> Edge(label="real-time communication") >> socketio
        server >> Edge(label="validate data") >> ajv
        server << Edge(label="HTTP JSON requests") >> users

    with Cluster("File System"):
        config_json = Windows("config.json")
        shell_scripts = Windows("hypnolog.sh")

    server << Edge(label="configuration") >> config_json
    users << Edge(label="command-line") >> shell_scripts