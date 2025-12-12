from diagrams import Diagram
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Nginx
from diagrams.onprem.container import Docker
from diagrams.onprem.workflow import Airflow
from diagrams.programming.language import Go
from diagrams.programming.language import Python

with Diagram("Minism Hotel Architecture", show=False, direction="TB"):
    client = Nginx("Game Client")
    
    master = Server("Hotel Master")
    rest_api = Go("REST API")
    rpc_server = Go("RPC Server")
    session_store = Go("Session Store")
    reaper = Go("Reaper")
    db = PostgreSQL("SQLite Database")
    
    spawner = Server("Hotel Spawner")
    spawner_rpc = Go("RPC Server")
    game_server_mgmt = Go("Game Server Management")
    
    shared_libs = Go("Shared Libraries")
    
    docker = Docker("Docker")
    compose = Docker("Docker Compose")
    makefile = Go("Makefile")
    
    tests = Python("Integration Tests")
    
    master >> rest_api
    master >> rpc_server
    master >> session_store
    master >> reaper
    rest_api >> db
    rpc_server >> db
    session_store >> db
    reaper >> db
    
    spawner >> spawner_rpc
    spawner >> game_server_mgmt
    
    client >> rest_api
    rpc_server >> spawner_rpc
    spawner_rpc >> game_server_mgmt
    
    docker >> compose
    
    tests >> rest_api