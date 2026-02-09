from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.programming.framework import Spring
from diagrams.onprem.database import MySQL
from diagrams.generic.network import Subnet
from diagrams.aws.network import Route53
from diagrams.aws.network import APIGateway
from diagrams.programming.language import Java

with Diagram("Pac Macro Game Server Architecture", show=False):
    with Cluster("Client Layer"):
        clients = Route53("Game Clients")
        api = APIGateway("REST API")

    with Cluster("Application Layer"):
        with Cluster("Controllers"):
            controllers = [
                Spring("AdminController"),
                Spring("PlayerController"),
                Spring("GameStateController"),
                Spring("PacdotController"),
                Spring("TagController")
            ]

        with Cluster("Managers"):
            managers = [
                Java("AdminManager"),
                Java("PlayerManager"), 
                Java("GameStateManager"),
                Java("PacdotManager"),
                Java("TagManager")
            ]

    with Cluster("Data Layer"):
        with Cluster("Registries"):
            registries = [
                Lambda("PlayerRegistry"),
                Lambda("GameStateRegistry"),
                Lambda("PacdotRegistry"),
                Lambda("TagRegistry")
            ]
            
        with Cluster("Repositories"):
            repos = [
                MySQL("PlayerRepository"),
                MySQL("PacdotRepository")
            ]

    # Connect components
    clients >> api
    api >> controllers
    
    for c, m in zip(controllers, managers):
        c >> m
        
    for m, r in zip(managers, registries):
        m >> r
        
    for r in registries:
        r >> repos