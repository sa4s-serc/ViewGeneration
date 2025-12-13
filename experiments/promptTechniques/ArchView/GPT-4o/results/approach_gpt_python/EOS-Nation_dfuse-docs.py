from diagrams import Diagram, Cluster
from diagrams.onprem.queue import Kafka
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Envoy
from diagrams.onprem.compute import Server
from diagrams.onprem.client import Client

with Diagram("dfuse-based System Architecture", show=False):
    client = Client("User or System")

    with Cluster("Microservices"):
        mindreader = Server("Mindreader")
        relayer = Server("Relayer")
        search = Server("Search")
        dgraphql = Server("DGraphQL")

    with Cluster("Data Storage"):
        bigtable = PostgreSQL("BigTable")
        tikv = PostgreSQL("TiKV")
        badger = PostgreSQL("Badger")

    client >> Envoy("gRPC") >> dgraphql
    mindreader >> Kafka("Data Streaming") >> relayer
    relayer >> search
    search >> dgraphql
    dgraphql >> bigtable
    dgraphql >> tikv
    dgraphql >> badger