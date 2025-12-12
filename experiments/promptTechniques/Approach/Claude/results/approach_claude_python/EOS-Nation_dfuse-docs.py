from diagrams import Diagram
from diagrams.custom import Custom
from diagrams.programming.framework import GraphQL
from diagrams.onprem.database import MongoDB, Cassandra
from diagrams.onprem.queue import Kafka
from diagrams.programming.framework import FastAPI
from diagrams.onprem.network import Nginx
from diagrams.onprem.client import Users

with Diagram("dfuse System Architecture", show=False):
    users = Users("API Clients")
    
    with Diagram("API Layer"):
        nginx = Nginx("Load Balancer")
        graphql = GraphQL("GraphQL API")
        api = FastAPI("REST API")

    with Diagram("Processing Layer"):
        kafka = Kafka("Event Stream")
        mindreader = Custom("Mindreader", "./mindreader.png")
        relayer = Custom("Relayer", "./relayer.png")
        search = Custom("Search", "./search.png")

    with Diagram("Storage Layer"):
        mongodb = MongoDB("Document Store")
        cassandra = Cassandra("Time Series Data")
        bigtable = Custom("BigTable", "./bigtable.png")

    # Connect components
    users >> nginx
    nginx >> graphql
    nginx >> api
    
    graphql >> kafka
    api >> kafka
    
    kafka >> mindreader
    mindreader >> relayer
    relayer >> search
    
    search >> mongodb
    search >> cassandra
    search >> bigtable