from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.onprem.network import Internet
from diagrams.onprem.compute import Server
from diagrams.onprem.client import Client

with Diagram("Architecture View", show=True, direction="TB"):
    net = Internet("Internet")

    with Cluster("Subsystem"):
        svc1 = Server("Service 1")
        svc2 = Server("Service 2")
        svc3 = Server("Service 3")

    client = Client("Client")

    net >> Edge(color="black", style="dotted") >> client
    client >> Edge(color="green", style="solid") >> svc1
    svc1 >> Edge(color="blue", style="dashed") >> svc2
    svc2 >> Edge(color="blue", style="dashed") >> svc3
    svc3 >> Edge(color="red", style="solid") >> net