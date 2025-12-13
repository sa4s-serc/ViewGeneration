from diagrams import Diagram, Cluster
from diagrams.onprem.queue import RabbitMQ
from diagrams.onprem.compute import Server
from diagrams.programming.language import NodeJS
from diagrams.generic.compute import Rack

with Diagram("IoT Serverless Architecture", show=False):
    with Cluster("IoT Devices Layer"):
        devices = [Server("IoT Device 1"), Server("IoT Device 2")]

    with Cluster("Message Brokers"):
        broker = RabbitMQ("RabbitMQ\nAMQP/MQTT")

    with Cluster("Serverless Functions"):
        functions = [
            Rack("Temperature\nProducer"),
            Rack("Temperature\nConsumer"),
            NodeJS("Logger")
        ]

    # Connect devices to message broker
    for device in devices:
        device >> broker

    # Connect broker to functions 
    broker >> functions[0]
    broker >> functions[1]
    broker >> functions[2]

    # Connect functions to each other for data flow
    functions[0] >> functions[1]
    functions[1] >> functions[2]