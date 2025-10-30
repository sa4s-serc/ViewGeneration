from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB, Route53
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import RabbitMQ
from diagrams.elastic.elasticsearch import Elasticsearch
from diagrams.azure.identity import ActiveDirectory
from diagrams.programming.framework import React

with Diagram("SmoresUnderflow Architecture", show=False):
    dns = Route53("DNS")
    lb = ELB("Load Balancer")
    
    with Cluster("Microservices"):
        auth_service = ActiveDirectory("Auth Service")
        user_service = EC2("User Service")
        question_service = EC2("Question Service")
        answer_service = EC2("Answer Service")
        media_service = EC2("Media Service")
        search_service = Elasticsearch("Search Service")
        frontend = React("React Frontend")
    
    dns >> lb >> [auth_service, user_service, question_service, answer_service, media_service, search_service, frontend]
    
    with Cluster("Asynchronous Communication"):
        mq = RabbitMQ("RabbitMQ")
        user_service >> mq >> question_service
        answer_service >> mq >> question_service
    
    with Cluster("Caching"):
        cache = Redis("Redis")
        user_service >> cache
        question_service >> cache
        answer_service >> cache
        media_service >> cache

    dns >> frontend