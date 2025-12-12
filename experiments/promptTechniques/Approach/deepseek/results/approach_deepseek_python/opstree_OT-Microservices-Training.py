from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.programming.framework import React
from diagrams.programming.framework import Spring
from diagrams.onprem.database import MySQL
from diagrams.elastic.elasticsearch import Elasticsearch
from diagrams.onprem.container import Docker
from diagrams.programming.language import Go
from diagrams.programming.language import Python

with Diagram("Employee Management System - Microservices Architecture", show=False, direction="TB"):
    user = User("End User")
    
    with Cluster("Frontend Layer"):
        webserver = Nginx("Web Server")
        frontend = React("React Frontend")
        webserver >> frontend
    
    with Cluster("API Gateway"):
        gateway = Spring("Spring Gateway")
    
    with Cluster("Microservices"):
        with Cluster("Go Services"):
            attendance = Go("Attendance Service")
            employee = Go("Employee Service")
            salary = Go("Salary Service")
        
        notification = Python("Notification Service")
    
    with Cluster("Data Layer"):
        mysql = MySQL("MySQL Database")
        elasticsearch = Elasticsearch("Elasticsearch")
    
    user >> webserver
    frontend >> gateway
    gateway >> [attendance, employee, salary, notification]
    attendance >> mysql
    employee >> elasticsearch
    salary >> elasticsearch
    notification >> elasticsearch