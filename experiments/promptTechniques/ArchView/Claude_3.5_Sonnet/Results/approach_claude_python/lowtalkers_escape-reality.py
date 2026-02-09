from diagrams import Diagram, Cluster
from diagrams.programming.framework import React
from diagrams.programming.language import NodeJS
from diagrams.aws.security import Cognito
from diagrams.aws.database import RDSMysqlInstance
from diagrams.aws.storage import S3
from diagrams.aws.network import CloudFront

with Diagram("VR Scene Explorer Architecture", show=False):
    with Cluster("Frontend"):
        frontend = React("React/A-Frame UI")

    with Cluster("Backend Services"):
        api = NodeJS("Node.js/Express API")
        auth = Cognito("Authentication")
        db = RDSMysqlInstance("MariaDB")
        storage = S3("Image Storage")
        cdn = CloudFront("CDN")

    # Frontend connections
    frontend >> api
    frontend >> cdn
    frontend >> auth

    # Backend connections
    api >> db
    api >> storage
    storage >> cdn
    api >> auth