from diagrams import Diagram, Cluster
from diagrams.onprem.database import MySQL
from diagrams.programming.language import NodeJS
from diagrams.onprem.container import Docker
from diagrams.aws.storage import S3
from diagrams.programming.framework import Laravel
from diagrams.onprem.network import Nginx

with Diagram("Food Service Architecture", show=False, direction="TB"):
    
    with Cluster("Application Layer"):
        api = NodeJS("REST API")
        web = Nginx("Web Server")
        router = Laravel("Router")

    with Cluster("Data Layer"):
        db = MySQL("MySQL Database")
        storage = S3("File Storage")

    with Cluster("Infrastructure"):
        docker = Docker("Docker Container")

    # Define relationships
    web >> api
    api >> router
    router >> db 
    router >> storage
    docker >> [web, db]

    # Add connection labels
    api - router >> db