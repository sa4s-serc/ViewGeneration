from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3
from diagrams.aws.analytics import ElasticsearchService
from diagrams.onprem.queue import Kafka
from diagrams.onprem.analytics import Flink
from diagrams.programming.framework import Spring, Angular
from diagrams.generic.device import Mobile
from diagrams.aws.general import InternetAlt1

with Diagram("Twitter Data Processing Architecture", show=False, direction="LR"):
    internet = InternetAlt1("Internet")
    
    with Cluster("Frontend Layer"):
        mobile_client = Mobile("Mobile Client")
        web_client = Angular("Web Client")
    
    with Cluster("Data Collection Layer"):
        with Cluster("Tweet Collector"):
            collector = Spring("Tweet Collector")
            twitter_api = InternetAlt1("Twitter API")
    
    with Cluster("Message Queue"):
        kafka = Kafka("Kafka Cluster")
    
    with Cluster("Processing Layer"):
        flink = Flink("Flink Processor")
    
    with Cluster("Storage Layer"):
        elasticsearch = ElasticsearchService("Elasticsearch")
    
    with Cluster("API Layer"):
        api_gateway = ELB("API Gateway")
        rest_api = Spring("REST API Server")
    
    with Cluster("Visualization Layer"):
        dashboard = Angular("Dashboard")
        heatmap = EC2("Heatmap Visualization")
    
    internet >> [mobile_client, web_client]
    twitter_api >> collector
    collector >> kafka
    kafka >> flink
    flink >> elasticsearch
    elasticsearch >> rest_api
    rest_api >> api_gateway
    api_gateway >> [dashboard, heatmap]
    [mobile_client, web_client] >> api_gateway