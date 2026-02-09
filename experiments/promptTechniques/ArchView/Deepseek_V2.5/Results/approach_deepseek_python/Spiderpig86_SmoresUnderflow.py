from diagrams import Diagram, Cluster
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import RabbitMQ
from diagrams.onprem.inmemory import Redis
from diagrams.elastic.elasticsearch import Elasticsearch
from diagrams.onprem.database import MongoDB
from diagrams.programming.framework import React
from diagrams.aws.compute import EC2

with Diagram("SmoresUnderflow Microservices Architecture", show=False, direction="TB"):
    frontend = React("React Frontend")
    
    with Cluster("Load Balancer"):
        nginx = Nginx("Nginx")
    
    with Cluster("Microservices"):
        with Cluster("User Services"):
            users = EC2("su-users")
            accounts = EC2("su-accounts")
        
        with Cluster("Question Services"):
            questions = EC2("su-questions")
            qu_questions = EC2("qu-questions")
            qu_answers = EC2("qu-answers")
        
        search = EC2("su-search")
        media = EC2("su-media")
    
    with Cluster("Message Queue"):
        rabbitmq = RabbitMQ("RabbitMQ")
    
    with Cluster("Data Layer"):
        with Cluster("Databases"):
            mongodb = MongoDB("MongoDB")
        
        with Cluster("Cache"):
            redis = Redis("Redis")
        
        with Cluster("Search Index"):
            elasticsearch = Elasticsearch("ElasticSearch")
    
    frontend >> nginx
    nginx >> [users, accounts, questions, search, media]
    
    questions >> rabbitmq
    rabbitmq >> [qu_questions, qu_answers]
    
    users >> mongodb
    users >> redis
    accounts >> mongodb
    questions >> mongodb
    qu_questions >> mongodb
    qu_questions >> elasticsearch
    qu_answers >> mongodb
    search >> mongodb
    search >> redis
    search >> elasticsearch
    media >> mongodb