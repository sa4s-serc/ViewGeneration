from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.database import PostgreSQL
from diagrams.programming.framework import React
from diagrams.aws.compute import EC2

with Diagram("Event Tracking System Architecture", show=False, direction="LR"):
    user = User("End User")
    
    with Cluster("Frontend"):
        frontend = React("React App")
        sdk = React("Tracking SDK")
    
    with Cluster("Backend Services"):
        gateway = EC2("Gateway Service")
        
        with Cluster("User Service"):
            user_service = EC2("User Service")
            user_db = PostgreSQL("User DB")
            user_service >> user_db
        
        with Cluster("Tracking Service"):
            tracking_service = EC2("Tracking Service")
            tracking_db = PostgreSQL("Tracking DB")
            tracking_service >> tracking_db
    
    redis = Redis("Redis Pub/Sub")
    
    user >> frontend
    frontend >> gateway
    gateway >> user_service
    gateway >> tracking_service
    gateway >> redis
    tracking_service >> redis
    sdk >> gateway