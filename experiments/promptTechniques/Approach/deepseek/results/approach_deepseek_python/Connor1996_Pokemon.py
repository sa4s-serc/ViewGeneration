from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import RabbitMQ
from diagrams.onprem.inmemory import Redis

with Diagram("Pokemon Game Architecture", show=False, direction="TB"):
    client = User("Client")
    
    with Cluster("Client Layer"):
        gui = Server("Qt GUI")
        client_logic = Server("Game Logic")
    
    with Cluster("Communication Layer"):
        socket_layer = Server("Socket Communication")
    
    with Cluster("Server Layer"):
        with Cluster("Multi-threaded Server"):
            server_instances = [
                Server("Server Thread 1"),
                Server("Server Thread 2"),
                Server("Server Thread 3")
            ]
        
        dispatcher = Server("Request Dispatcher")
        
        with Cluster("Game Logic"):
            pokemon_factory = Server("Pokemon Factory")
            battle_logic = Server("Battle Logic")
    
    with Cluster("Data Layer"):
        orm = Server("ORM Layer")
        database = PostgreSQL("SQLite Database")
        cache = Redis("Cache")
    
    client >> gui
    gui >> client_logic
    client_logic >> socket_layer
    socket_layer >> server_instances
    server_instances >> dispatcher
    dispatcher >> battle_logic
    battle_logic >> pokemon_factory
    pokemon_factory >> orm
    orm >> database
    dispatcher >> cache
    cache >> orm