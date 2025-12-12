from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS
from diagrams.aws.network import APIGateway
from diagrams.custom import Custom
from diagrams.gcp.network import LoadBalancing
from diagrams.onprem.client import Users
from diagrams.programming.framework import React

with Diagram("Bee Green Architecture", show=False):
    users = Users("End Users")

    with Cluster("Frontend"):
        chrome = Custom("Chrome Extension", "./extension.png")
        client = React("React Client")

    with Cluster("Backend"):
        api = APIGateway("API Gateway")
        
        with Cluster("Server Components"):
            lb = LoadBalancing("Load Balancer")
            server = Lambda("LoopBack 4\nServer")
            db = RDS("Cloudant DB")

    users >> chrome
    users >> client
    
    chrome >> api
    client >> api
    
    api >> lb
    lb >> server
    server >> db