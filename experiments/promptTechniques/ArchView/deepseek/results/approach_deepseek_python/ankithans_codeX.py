from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.programming.framework import React, FastAPI
from diagrams.onprem.database import SQLite
from diagrams.onprem.compute import Server
from diagrams.aws.ml import Sagemaker
from diagrams.gcp.ml import AIPlatform
from diagrams.gcp.translate import Translate

with Diagram("CodeX Web Application Architecture", show=False, direction="LR"):
    user = User("User")
    
    with Cluster("Frontend"):
        frontend = React("ReactJS App")
        components = [
            React("Navbar"),
            React("PseudoCode"),
            React("Warnings"), 
            React("Compile")
        ]
        frontend - components
    
    with Cluster("Backend API Gateway"):
        backend = FastAPI("FastAPI Gateway")
        
        with Cluster("Routes"):
            routes = [
                Server("compile.py"),
                Server("convertPseudo.py"),
                Server("warnings.py"),
                Server("translatePseudo.py"),
                Server("shareCode.py"),
                Server("flowchart.py")
            ]
        
        with Cluster("Services"):
            services = [
                Server("pylint.py"),
                Server("pseudo_code.py"),
                Server("hackerearth_compile.py"),
                Server("flowchart.py")
            ]
    
    with Cluster("External Services"):
        external = [
            Sagemaker("HackerEarth API"),
            Translate("Google Translate"),
            AIPlatform("Pylint")
        ]
    
    with Cluster("Data Storage"):
        database = SQLite("SQLite Database")
    
    user >> frontend >> backend
    backend >> routes
    routes >> services
    services >> external
    backend >> database