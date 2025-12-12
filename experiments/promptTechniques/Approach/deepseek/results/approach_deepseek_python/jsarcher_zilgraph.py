from diagrams import Diagram
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.elastic.elasticsearch import Elasticsearch
from diagrams.onprem.database import MongoDB
from diagrams.onprem.compute import Server
from diagrams.onprem.inmemory import Redis
from diagrams.programming.language import Python
from diagrams.custom import Custom

with Diagram("Zilgraph Architecture", show=False, direction="LR"):
    user = User("User")
    
    nginx = Nginx("Nginx")
    
    bokeh_dashboard = Custom("Bokeh Dashboard", "./bokeh.png")
    kibana = Custom("Kibana Dashboard", "./kibana.png")
    
    crawler = Server("Zilcrawler")
    aggregator = Server("Zillog Aggregator")
    zilswap = Server("Zilswap Processor")
    
    elasticsearch = Elasticsearch("Elasticsearch")
    mongodb = MongoDB("MongoDB")
    
    blockchain = Custom("Zilliqa Blockchain", "./blockchain.png")
    
    user >> nginx
    nginx >> bokeh_dashboard
    nginx >> kibana
    
    crawler >> blockchain
    crawler >> elasticsearch
    
    aggregator >> elasticsearch
    aggregator >> mongodb
    
    zilswap >> blockchain
    zilswap >> elasticsearch
    
    bokeh_dashboard >> mongodb
    kibana >> elasticsearch