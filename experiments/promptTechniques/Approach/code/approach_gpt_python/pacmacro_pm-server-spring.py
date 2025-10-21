from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.onprem.client import Client
from diagrams.generic.database import SQL

with Diagram("Pac Macro Game Server Architecture", show=False):
    client = Client("Clients")

    with Cluster("Spring Boot RESTful Application"):
        controllers = [
            EC2("AdminController"),
            EC2("PlayerController"),
            EC2("GameStateController"),
            EC2("PacdotController"),
            EC2("TagController"),
            EC2("MetricsController"),
            EC2("HomeController")
        ]

        with Cluster("Manager Layer"):
            admin_manager = EC2("AdminManager")
            player_manager = EC2("PlayerManager")
            game_state_manager = EC2("GameStateManager")
            pacdot_manager = EC2("PacdotManager")
            tag_manager = EC2("TagManager")

        with Cluster("Registry Layer"):
            player_registry = SQL("PlayerRegistry")
            game_state_registry = SQL("GameStateRegistry")
            pacdot_registry = SQL("PacdotRegistry")
            tag_registry = SQL("TagRegistry")

        with Cluster("Repository Layer"):
            player_repository = SQL("PlayerRepository")
            pacdot_repository = SQL("PacdotRepository")

        with Cluster("Utilities"):
            utilities = EC2("Utilities")

    client >> controllers
    for controller, manager in zip(controllers, [admin_manager, player_manager, game_state_manager, pacdot_manager, tag_manager]):
        controller >> manager
    admin_manager >> player_registry
    player_manager >> player_registry
    game_state_manager >> game_state_registry
    pacdot_manager >> pacdot_registry
    tag_manager >> tag_registry
    player_registry >> player_repository
    pacdot_registry >> pacdot_repository
    game_state_registry >> player_repository
    managers = [admin_manager, player_manager, game_state_manager, pacdot_manager, tag_manager]
    for manager in managers:
        manager >> utilities