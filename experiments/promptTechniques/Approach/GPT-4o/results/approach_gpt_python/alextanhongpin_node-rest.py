from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.database import MySQL
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Nginx
from diagrams.programming.language import Nodejs
from diagrams.generic.compute import Rack

with Diagram("Food Service Application Architecture", show=True):
    client = User("User")

    with Cluster("Food Service Application"):
        nodejs = Nodejs("NodeJS")

        with Cluster("Onion Architecture"):
            model = Rack("Model")
            store = Rack("Store")
            route = Rack("Route")

            model >> store
            route >> model
            nodejs >> route

    db = MySQL("MySQL Database")
    docker = Docker("Docker")
    nginx = Nginx("Nginx")

    client >> nginx >> nodejs
    store >> db
    nodejs >> docker
    db >> docker