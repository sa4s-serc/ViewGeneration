from diagrams import Diagram, Cluster
from diagrams.aws.storage import S3
from diagrams.onprem.client import User
from diagrams.onprem.database import Mariadb
from diagrams.onprem.compute import Server
from diagrams.programming.language import Nodejs
from diagrams.programming.framework import React
from diagrams.generic.os import Linux

with Diagram("VR Scene Exploration Application Architecture", show=False, direction="TB"):
    client = User("User Browser")

    with Cluster("Client-side"):
        react_app = React("React App")
        a_frame = Linux("A-Frame VR")
        client >> react_app >> a_frame

    with Cluster("Server-side"):
        node_server = Nodejs("Node.js Server")
        express = Server("Express.js")
        react_app >> express
        node_server >> express

        with Cluster("Database"):
            mariadb = Mariadb("MariaDB")
            express >> mariadb

        with Cluster("Storage"):
            aws_s3 = S3("AWS S3")
            express >> aws_s3

    client >> react_app
    express >> react_app