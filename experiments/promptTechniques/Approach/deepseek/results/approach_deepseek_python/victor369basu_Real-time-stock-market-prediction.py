from diagrams import Diagram, Cluster
from diagrams.onprem.queue import Kafka
from diagrams.onprem.database import MongoDB
from diagrams.onprem.compute import Server
from diagrams.programming.language import Nodejs
from diagrams.generic.blank import Blank

with Diagram("Stock Market Prediction System", show=False, direction="LR"):
    with Cluster("Data Ingestion"):
        producer = Nodejs("producer.js")
        csv_source = Blank("CSV Data Source")
        
    with Cluster("Message Bus"):
        kafka = Kafka("Kafka")
        
    with Cluster("Data Processing"):
        consumer = Nodejs("consumer.js")
        ml_consumer = Nodejs("ml_consumer.js")
        pre_process = Nodejs("pre_process.js")
        
    with Cluster("Machine Learning"):
        tf_train = Nodejs("tf_train.js")
        tf_validate = Nodejs("tf_validate.js")
        tf_model = Nodejs("tf_model.js")
        
    with Cluster("Application Server"):
        server = Nodejs("server.js")
        
    with Cluster("Data Storage"):
        mongodb = MongoDB("MongoDB")
        
    with Cluster("Configuration"):
        config = Nodejs("config.js")
        instantiate_db = Nodejs("InstantiateDB.js")

    csv_source >> producer >> kafka
    kafka >> consumer >> mongodb
    kafka >> ml_consumer >> pre_process
    pre_process >> tf_model
    tf_train >> tf_model
    tf_validate >> tf_model
    tf_model >> mongodb
    server >> tf_train
    server >> tf_validate
    config >> producer
    config >> consumer
    config >> ml_consumer
    config >> tf_train
    config >> tf_validate
    instantiate_db >> mongodb