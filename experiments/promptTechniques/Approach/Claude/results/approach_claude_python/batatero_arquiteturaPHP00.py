from diagrams import Diagram
from diagrams.programming.framework import Laravel
from diagrams.onprem.database import MySQL, Mongodb
from diagrams.programming.language import Php
from diagrams.onprem.queue import RabbitMQ

with Diagram("CodeIgniter Data Access Layer Architecture", show=False):
    
    # Core components
    controller = Php("Controller")
    facade = Laravel("Facade")
    business = Php("Business Logic") 
    dao = Php("DAO")
    
    # Data stores
    db = MySQL("MySQL")
    mongo = Mongodb("MongoDB")
    queue = RabbitMQ("Message Queue")
    
    # Flow
    controller >> facade
    facade >> business
    business >> dao
    
    # Data access
    dao >> db
    dao >> mongo
    business >> queue
