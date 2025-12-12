from diagrams import Diagram
from diagrams.onprem.client import User
from diagrams.onprem.database import Postgresql
from diagrams.programming.framework import React, DotNet
from diagrams.aws.network import APIGateway

with Diagram("Nightingale Reference Client Architecture", show=False, direction="TB"):
    user = User("Jurisdiction User")
    
    ui = React("React UI")
    api = DotNet(".NET API")
    background = DotNet("TimedHostedService")
    db = Postgresql("PostgreSQL")
    nvss_api = APIGateway("NVSS API Server")
    
    user >> ui
    ui >> api
    api >> db
    background >> db
    api >> nvss_api
    background >> nvss_api