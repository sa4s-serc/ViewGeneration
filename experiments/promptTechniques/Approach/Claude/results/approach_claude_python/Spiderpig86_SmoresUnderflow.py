from diagrams import Diagram, Cluster
from diagrams.onprem.database import MongoDB
from diagrams.onprem.queue import RabbitMQ
from diagrams.onprem.inmemory import Redis
from diagrams.elastic.elasticsearch import Elasticsearch
from diagrams.onprem.network import Nginx
from diagrams.onprem.compute import Server
from diagrams.programming.framework import React
from diagrams.programming.language import NodeJS

with Diagram("SmoresUnderflow Architecture", show=False, direction="TB"):
    with Cluster("Frontend"):
        frontend = React("React Frontend")

    with Cluster("API Gateway"):
        nginx = Nginx("Nginx")

    with Cluster("Microservices"):
        users = NodeJS("Users Service")
        questions = NodeJS("Questions Service")
        answers = NodeJS("Answers Service")
        search = NodeJS("Search Service")
        media = NodeJS("Media Service")
        accounts = NodeJS("Accounts Service")

    with Cluster("Message Queue"):
        queue = RabbitMQ("RabbitMQ")

    with Cluster("Databases"):
        mongodb = MongoDB("MongoDB")
        redis = Redis("Redis")
        elastic = Elasticsearch("ElasticSearch")

    # Frontend connections
    frontend >> nginx

    # API Gateway connections 
    nginx >> [users, questions, answers, search, media, accounts]

    # Service connections
    users >> mongodb
    users >> redis
    questions >> mongodb
    questions >> redis
    questions >> elastic
    answers >> mongodb
    answers >> redis
    search >> elastic
    media >> mongodb

    # Message queue connections
    [questions, answers] >> queue
    queue >> [questions, answers]