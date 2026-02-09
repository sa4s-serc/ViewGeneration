from diagrams import Diagram
from diagrams.generic.device import Tablet
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka
from diagrams.programming.framework import FastAPI
from diagrams.programming.framework import React

with Diagram("System Architecture", show=False, direction="TB"):
    user = User("User")
    
    with Diagram("Frontend Layer"):
        web_app = React("Web Application")
        mobile_app = Tablet("Mobile App")
    
    with Diagram("API Gateway"):
        gateway = Nginx("API Gateway")
    
    with Diagram("Backend Services"):
        auth_service = FastAPI("Auth Service")
        order_service = FastAPI("Order Service")
        payment_service = FastAPI("Payment Service")
        notification_service = FastAPI("Notification Service")
    
    with Diagram("Data Layer"):
        main_db = PostgreSQL("Main Database")
        cache = Redis("Cache")
        message_queue = Kafka("Message Queue")
    
    user >> web_app
    user >> mobile_app
    web_app >> gateway
    mobile_app >> gateway
    
    gateway >> auth_service
    gateway >> order_service
    gateway >> payment_service
    
    auth_service >> main_db
    order_service >> main_db
    payment_service >> main_db
    
    order_service >> cache
    payment_service >> cache
    
    order_service >> message_queue
    payment_service >> message_queue
    message_queue >> notification_service
    notification_service >> main_db