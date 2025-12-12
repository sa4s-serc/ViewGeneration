from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Internet
from diagrams.programming.language import Javascript
from diagrams.programming.language import Erlang

with Diagram("Earth Defender Architecture", show=False, direction="TB"):
    internet = Internet("Internet")
    
    with Cluster("Client Side (Three.js)"):
        user = User("Player")
        browser = Javascript("Browser")
        game = Javascript("Game")
        game_client = Javascript("GameClient")
        game_dom = Javascript("GameDOMHandler")
        game_elements = Javascript("GameElements")
        texture_loader = Javascript("TextureLoader")
        
        user >> browser
        browser >> game
        game >> game_client
        game >> game_dom
        game >> game_elements
        game_elements >> texture_loader

    with Cluster("Server Side (Erlang/OTP)"):
        with Cluster("Supervision Tree"):
            supervisor = Erlang("earth_defender_sup")
            app = Erlang("earth_defender_app")
            cowboy = Erlang("Cowboy Server")
            
            supervisor >> app
            app >> cowboy

        with Cluster("Core Modules"):
            websocket = Erlang("websocket_handler")
            room = Erlang("room")
            player = Erlang("player")
            local_rooms = Erlang("local_rooms_state")
            slave = Erlang("slave_handler")
            monitor = Erlang("monitor_mesh")
            utils = Erlang("utils")
            
            cowboy >> websocket
            websocket >> room
            websocket >> player
            room >> local_rooms
            supervisor >> slave
            supervisor >> monitor
            room >> utils
            player >> utils

    game_client >> internet >> websocket
    slave >> slave