from diagrams import Diagram, Cluster, Edge
from diagrams.generic.device import Mobile
from diagrams.generic.storage import Storage
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Rabbitmq
from diagrams.onprem.database import Mongodb
from diagrams.programming.language import Python

with Diagram("Serverless IoT Architecture", show=False):
    with Cluster("IoT Devices"):
        device1 = Mobile("IoT Device 1")
        device2 = Mobile("IoT Device 2")

    with Cluster("Serverless Platform"):
        nuclio = Server("Nuclio")
        with Cluster("Functions"):
            producer_fn = Python("Producer Function")
            consumer_fn = Python("Consumer Function")

    with Cluster("Message Broker"):
        rabbitmq = Rabbitmq("RabbitMQ")

    with Cluster("Data Storage"):
        db = Mongodb("MongoDB")

    with Cluster("Client"):
        client = Nginx("Client")

    device1 >> Edge(label="MQTT/AMQP") >> rabbitmq
    device2 >> Edge(label="MQTT/AMQP") >> rabbitmq

    rabbitmq >> Edge(label="Event Trigger") >> producer_fn
    producer_fn >> Edge(label="Data Processing") >> consumer_fn
    consumer_fn >> Edge(label="Store Data") >> db

    client >> Edge(label="Retrieve Data") >> db