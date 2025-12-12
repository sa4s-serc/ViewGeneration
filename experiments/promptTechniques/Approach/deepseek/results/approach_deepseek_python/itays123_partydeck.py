from diagrams import Diagram, Cluster
from diagrams.onprem.client import Users
from diagrams.programming.framework import React
from diagrams.programming.language import Java
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Internet
from diagrams.onprem.container import Docker

with Diagram("Partydeck Microservices Architecture", show=False, direction="TB"):
    internet = Internet("Internet")
    users = Users("Players")
    
    with Cluster("Frontend Layer"):
        panel = React("Panel (React)\nDeck Management\nUser Auth")
        game_client = React("Game (React)\nGameplay UI")
    
    with Cluster("Backend Layer"):
        server = Java("Server (Java)\nWebSocket Server\nGame Logic\nREST API")
        database = PostgreSQL("Database\nGame State\nUser Data")
    
    users >> internet
    internet >> panel
    internet >> game_client
    panel >> server
    game_client >> server
    server >> database