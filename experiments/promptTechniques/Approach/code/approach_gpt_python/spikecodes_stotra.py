from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.devtools import Codebuild
from diagrams.onprem.client import Users
from diagrams.onprem.database import Mongodb
from diagrams.onprem.compute import Server
from diagrams.programming.framework import React
from diagrams.programming.framework import Express

with Diagram("Stotra Full-Stack Architecture", show=False):
    users = Users("Users")

    with Cluster("AWS Cloud"):
        amplify = Codebuild("Amplify")
        ec2 = EC2("Elastic Cloud Compute")

    with Cluster("Frontend (React)"):
        react = React("React App")
        react - Edge(label="axios REST API") - ec2

    with Cluster("Backend (Node.js/Express)"):
        nodejs = Express("Node.js Backend")
        server = Server("Docker Container")

        ec2 - server
        server - nodejs

        with Cluster("Database"):
            mongodb = Mongodb("MongoDB Atlas")
            nodejs >> Edge(label="Mongoose") >> mongodb

    users >> amplify >> react
    nodejs >> Edge(label="External API Calls") >> Server("Yahoo Finance\nAlpha Vantage\nNewsFilter")