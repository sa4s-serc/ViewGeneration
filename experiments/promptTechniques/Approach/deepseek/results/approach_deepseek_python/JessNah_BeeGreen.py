from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.programming.framework import React
from diagrams.onprem.compute import Server
from diagrams.aws.database import Dynamodb

with Diagram("Bee Green Application Architecture", show=False, direction="TB"):
    user = User("Online Shopper")
    
    with Cluster("Chrome Extension"):
        extension = React("Bee Green Extension")
        background = Server("Background Script")
        content = Server("Content Script")
        popup = Server("Popup")
        storage = Dynamodb("Local Storage")
        
        extension >> background
        background >> content
        extension >> popup
        extension >> storage
    
    with Cluster("Client Website"):
        client = React("React Client")
        dashboard = React("Dashboard")
        contribute = React("Contribute")
        
        client >> dashboard
        client >> contribute
    
    with Cluster("LoopBack 4 Server"):
        server = Server("API Server")
        api = Server("REST API")
        cloudant = Dynamodb("IBM Cloudant")
        processing = Server("Data Processing")
        
        server >> api
        api >> cloudant
        server >> processing
    
    user >> extension
    extension >> api
    client >> api
    user >> client