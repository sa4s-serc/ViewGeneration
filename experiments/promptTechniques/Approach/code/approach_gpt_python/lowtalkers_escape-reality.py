from diagrams import Diagram
from diagrams.programming.framework import React
from diagrams.onprem.database import Mariadb
from diagrams.programming.language import NodeJS
from diagrams.aws.storage import S3
from diagrams.firebase.develop import Authentication

with Diagram("VR Scene Exploration Application Architecture", show=False):
    react_client = React("React Client")
    node_server = NodeJS("Node.js Server")
    database = Mariadb("MariaDB")
    storage = S3("AWS S3")
    auth = Authentication("User Authentication")

    react_client >> node_server
    node_server >> database
    node_server >> storage
    node_server >> auth