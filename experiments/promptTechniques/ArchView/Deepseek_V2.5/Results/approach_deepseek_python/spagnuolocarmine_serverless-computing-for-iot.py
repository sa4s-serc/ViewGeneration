from diagrams import Diagram, Cluster
from diagrams.onprem.queue import RabbitMQ
from diagrams.onprem.compute import Server
from diagrams.generic.device import Tablet
from diagrams.onprem.container import Docker
from diagrams.programming.language import Nodejs

with Diagram("Serverless IoT Architecture", show=False, direction="LR"):
    iot_devices = Tablet("IoT Devices")
    
    with Cluster("Message Broker"):
        rabbitmq = RabbitMQ("RabbitMQ")
    
    with Cluster("Serverless Platform"):
        nuclio = Server("Nuclio")
        
        with Cluster("Functions"):
            producer = Docker("Producer Function")
            consumer = Docker("Consumer Function")
    
    logger = Nodejs("Logger")
    
    iot_devices >> rabbitmq
    rabbitmq >> producer
    rabbitmq >> consumer
    consumer >> logger