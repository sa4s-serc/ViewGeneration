from diagrams import Diagram, Cluster
from diagrams.onprem.client import Users
from diagrams.onprem.network import Nginx
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker
from diagrams.onprem.queue import Rabbitmq
from diagrams.onprem.database import Postgresql

with Diagram("Airline Microservices Architecture", show=False, direction="LR"):

    user = Users("User")

    with Cluster("API Gateway"):
        api_gateway = Nginx("YARP")

    with Cluster("Microservices"):
        with Cluster("Identity Service"):
            identity_service = Server("Identity API")
            identity_db = Postgresql("Identity DB")
            identity_service >> identity_db

        with Cluster("Flight Service"):
            flight_service = Server("Flight API")
            flight_db = Postgresql("Flight DB")
            flight_service >> flight_db

        with Cluster("Passenger Service"):
            passenger_service = Server("Passenger API")
            passenger_db = Postgresql("Passenger DB")
            passenger_service >> passenger_db

        with Cluster("Reservation Service"):
            reservation_service = Server("Reservation API")
            reservation_db = Postgresql("Reservation DB")
            reservation_service >> reservation_db

        services = [identity_service, flight_service, passenger_service, reservation_service]

    event_bus = Rabbitmq("RabbitMQ")

    docker = Docker("Docker")

    user >> api_gateway >> services
    services >> event_bus
    docker << services