from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.programming.framework import React
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import Postgresql
from diagrams.programming.language import Nodejs

with Diagram("Restaurant Reservation Application Architecture", show=False, direction="TB"):
    user = User("End User")
    
    with Cluster("Frontend Layer"):
        frontend = React("React App")
    
    with Cluster("Backend Layer"):
        with Cluster("API Layer"):
            api = Nodejs("Express API")
        
        with Cluster("Business Logic"):
            reservations = Nodejs("Reservations\nController")
            tables = Nodejs("Tables\nController")
        
        with Cluster("Data Access"):
            reservations_service = Nodejs("Reservations\nService")
            tables_service = Nodejs("Tables\nService")
    
    with Cluster("Data Layer"):
        database = Postgresql("PostgreSQL")
    
    user >> frontend
    frontend >> api
    api >> reservations
    api >> tables
    reservations >> reservations_service
    tables >> tables_service
    reservations_service >> database
    tables_service >> database