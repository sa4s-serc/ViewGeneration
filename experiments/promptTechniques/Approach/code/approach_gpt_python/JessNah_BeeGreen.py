from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.onprem.client import Client
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker
from diagrams.onprem.database import Mongodb
from diagrams.programming.framework import React

with Diagram("Bee Green Application Architecture", show=False, direction="TB"):

    with Cluster("Chrome Extension"):
        extension = Custom("Chrome Extension", "./icons/chrome.png")
        background = Custom("background.ts", "./icons/typescript.png")
        content_script = Custom("contentScript.tsx", "./icons/react.png")
        popup = Custom("popup.tsx", "./icons/react.png")
        extension >> Edge(label="Listens for tab updates") >> background
        background >> Edge(label="Injects content scripts") >> content_script
        content_script >> Edge(label="Displays side tab") >> popup

    with Cluster("Client Website"):
        client = React("React Client")
        dashboard = Custom("DashBoard.js", "./icons/react.png")
        contribute = Custom("Contribute.js", "./icons/react.png")
        client >> Edge(label="Renders dashboard") >> dashboard
        client >> Edge(label="Renders contribute page") >> contribute

    with Cluster("Server"):
        server = Server("LoopBack 4 Server")
        rest_api = Custom("REST API", "./icons/rest.png")
        database = Mongodb("IBM Cloudant")
        server >> Edge(label="Exposes") >> rest_api
        rest_api >> Edge(label="Manages data") >> database

    client >> Edge(label="Fetches/Sends data") >> server
    extension >> Edge(label="Communicates with") >> server