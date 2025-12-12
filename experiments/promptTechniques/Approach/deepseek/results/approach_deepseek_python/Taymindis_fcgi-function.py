from diagrams import Diagram
from diagrams.onprem.network import Nginx
from diagrams.onprem.compute import Server
from diagrams.programming.language import C, Cpp
from diagrams.onprem.container import Docker
from diagrams.onprem.client import User

with Diagram("FastCGI Function Handler Framework Architecture", show=False, direction="TB"):
    user = User("HTTP Client")
    webserver = Nginx("Web Server\n(Nginx/Apache)")
    fastcgi_server = Server("FastCGI Server\n(ffunc.c)")
    function_handlers = [
        C("getProfile\nHandler"),
        Cpp("postProfile\nHandler"),
        C("postError\nHandler")
    ]
    docker = Docker("Docker\nContainer")
    
    user >> webserver
    webserver >> fastcgi_server
    fastcgi_server >> function_handlers[0]
    fastcgi_server >> function_handlers[1]
    fastcgi_server >> function_handlers[2]
    docker >> webserver
    docker >> fastcgi_server