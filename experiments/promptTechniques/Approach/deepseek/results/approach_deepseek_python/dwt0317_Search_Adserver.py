from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.programming.language import Java
from diagrams.programming.framework import Spring
from diagrams.elastic.elasticsearch import Elasticsearch
from diagrams.generic.database import SQL

with Diagram("Search Ad Server Architecture", show=False, direction="TB"):
    user = User("User")
    
    with Cluster("Frontend Layer"):
        frontend = Nginx("Web Interface")
    
    with Cluster("Application Layer"):
        with Cluster("Servlets"):
            es_servlet = Java("ESServlet")
            bing_servlet = Java("BingServlet")
        
        with Cluster("Business Logic"):
            ad_retrieval = Java("AdRetrieval")
            rewriting_handler = Java("RewritingHandler")
            config = Java("Config")
    
    with Cluster("External Services"):
        bing_api = EC2("Bing Search API")
        thrift_service = EC2("Thrift Service")
        flume = EC2("Flume")
    
    with Cluster("Data Layer"):
        with Cluster("Databases"):
            mariadb = SQL("MariaDB")
            elasticsearch = Elasticsearch("Elasticsearch")
        
        with Cluster("Caching"):
            cache = Redis("LRU Cache")
    
    with Cluster("Configuration"):
        properties = S3("Property Files")
    
    # Connections
    user >> frontend
    frontend >> es_servlet
    frontend >> bing_servlet
    es_servlet >> elasticsearch
    bing_servlet >> bing_api
    es_servlet >> ad_retrieval
    bing_servlet >> ad_retrieval
    ad_retrieval >> rewriting_handler
    rewriting_handler >> thrift_service
    ad_retrieval >> mariadb
    ad_retrieval >> elasticsearch
    elasticsearch >> cache
    config >> properties
    ad_retrieval >> flume