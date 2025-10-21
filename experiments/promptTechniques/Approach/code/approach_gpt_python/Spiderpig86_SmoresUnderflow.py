from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.onprem.compute import Server
from diagrams.onprem.queue import RabbitMQ
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.database import Mongodb
from diagrams.onprem.search import ElasticSearch
from diagrams.programming.language import React

with Diagram("SmoresUnderflow Architecture", show=False, direction="TB"):
    user = User("User")

    with Cluster("Frontend"):
        frontend = React("su-frontend")

    with Cluster("API Gateway"):
        nginx = Nginx("Nginx")

    with Cluster("Microservices"):
        with Cluster("User Management"):
            users_service = Server("su-users")
            accounts_service = Server("su-accounts")

        with Cluster("Q&A Handling"):
            questions_service = Server("su-questions")
            answers_service = Server("su-answers")
            qu_questions_queue = RabbitMQ("qu-questions")
            qu_answers_queue = RabbitMQ("qu-answers")
            qu_delete_questions_queue = RabbitMQ("qu-delete-questions")

        with Cluster("Search"):
            search_service = Server("su-search")

        with Cluster("Media Handling"):
            media_service = Server("su-media")

    with Cluster("Databases & Caching"):
        redis_cache = Redis("Redis")
        mongo_db = Mongodb("MongoDB")
        es_db = ElasticSearch("ElasticSearch")

    user >> frontend
    frontend >> nginx

    nginx >> Edge(label="JWT Auth") >> users_service
    nginx >> accounts_service

    nginx >> questions_service
    nginx >> answers_service

    questions_service >> qu_questions_queue
    answers_service >> qu_answers_queue

    qu_questions_queue >> mongo_db
    qu_answers_queue >> mongo_db
    qu_delete_questions_queue >> mongo_db

    nginx >> search_service
    search_service >> es_db

    nginx >> media_service

    users_service >> redis_cache
    accounts_service >> redis_cache
    questions_service >> redis_cache
    answers_service >> redis_cache

    users_service >> mongo_db
    accounts_service >> mongo_db
    questions_service >> mongo_db
    answers_service >> mongo_db