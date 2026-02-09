from diagrams import Diagram
from diagrams.onprem.network import Yarp
from diagrams.onprem.container import Docker
from diagrams.onprem.queue import RabbitMQ
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.security import Vault

with Diagram("Airline Microservices Architecture", show=False, direction="LR"):
    api_gateway = Yarp("API Gateway")
    
    identity_service = Vault("Identity Service")
    flight_service = Docker("Flight Service")
    passenger_service = Docker("Passenger Service")
    reservation_service = Docker("Reservation Service")
    
    message_broker = RabbitMQ("RabbitMQ")
    
    identity_db = PostgreSQL("Identity DB")
    flight_db = PostgreSQL("Flight DB")
    passenger_db = PostgreSQL("Passenger DB")
    reservation_db = PostgreSQL("Reservation DB")
    
    cache = Redis("Cache")
    
    api_gateway >> [identity_service, flight_service, passenger_service, reservation_service]
    
    identity_service >> identity_db
    flight_service >> flight_db
    passenger_service >> passenger_db
    reservation_service >> reservation_db
    
    flight_service >> message_broker
    reservation_service >> message_broker
    passenger_service >> message_broker
    
    flight_service >> cache
    reservation_service >> cache