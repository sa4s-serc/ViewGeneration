from diagrams import Diagram, Cluster
from diagrams.onprem.client import Client
from diagrams.onprem.compute import Server
from diagrams.onprem.database import Mongodb
from diagrams.onprem.queue import Kafka
from diagrams.programming.language import NodeJS

with Diagram("Stock Market Prediction System", show=False):
    client = Client("User")

    with Cluster("Kafka Data Pipeline"):
        producer = NodeJS("producer.js")
        consumer = NodeJS("consumer.js")
        ml_consumer = NodeJS("ml_consumer.js")
        create_topics = NodeJS("createTopics.js")
        
        producer >> Kafka("Stock Data Topic") >> consumer
        ml_consumer >> Kafka("Real-time Prediction Topic")

    with Cluster("Machine Learning"):
        pre_process = NodeJS("pre_process.js")
        tf_train = NodeJS("tf_train.js")
        tf_validate = NodeJS("tf_validate.js")
        tf_model = NodeJS("tf_model.js")
        
        pre_process >> tf_train
        tf_train >> tf_validate
        tf_validate >> tf_model

    with Cluster("MongoDB Data Storage"):
        db = Mongodb("MongoDB")
        instantiate_db = NodeJS("InstantiateDB.js")

        consumer >> instantiate_db >> db
        ml_consumer >> db
        tf_validate >> db

    with Cluster("Web Server"):
        server = Server("server.js")
        config = NodeJS("config.js")
        
        client >> server
        server >> create_topics

    create_topics >> Kafka("Kafka Topics")
    server >> [config, instantiate_db]