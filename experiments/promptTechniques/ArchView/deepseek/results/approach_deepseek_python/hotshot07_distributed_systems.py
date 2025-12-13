from diagrams import Diagram, Cluster
from diagrams.aws.database import Dynamodb
from diagrams.aws.security import Cognito
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.programming.framework import React
from diagrams.programming.framework import Flask

with Diagram("Doping Control System Architecture", show=False, direction="TB"):
    user = User("Athlete/User")
    
    with Cluster("Frontend"):
        frontend = React("React App")
    
    with Cluster("Backend Microservices"):
        with Cluster("Authentication Service"):
            auth = Cognito("Auth Service")
        
        with Cluster("Account Management"):
            account = Flask("Account Service")
        
        with Cluster("Athlete Availability"):
            availability = Flask("Availability Service")
        
        with Cluster("Test Scheduling"):
            scheduling = Flask("Scheduling Service")
        
        with Cluster("Test Reporting"):
            reporting = Flask("Reporting Service")
    
    with Cluster("Data Storage"):
        database = Dynamodb("DynamoDB")
    
    with Cluster("Infrastructure"):
        with Cluster("Kubernetes Cluster"):
            k8s = Server("K8s Cluster")
        
        with Cluster("CI/CD"):
            cicd = Server("GitHub Actions")
    
    user >> frontend
    frontend >> auth
    frontend >> account
    frontend >> availability
    frontend >> scheduling
    frontend >> reporting
    
    auth >> database
    account >> database
    availability >> database
    scheduling >> database
    reporting >> database
    
    k8s >> frontend
    k8s >> auth
    k8s >> account
    k8s >> availability
    k8s >> scheduling
    k8s >> reporting
    
    cicd >> k8s