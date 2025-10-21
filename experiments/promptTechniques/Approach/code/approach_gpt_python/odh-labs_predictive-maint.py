from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.onprem.client import User
from diagrams.onprem.queue import Kafka
from diagrams.onprem.compute import Server
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.storage import Minio
from diagrams.onprem.ci import Github

with Diagram("Predictive Maintenance System", show=False):
    user = User("Web User")

    with Cluster("Microservices Architecture"):
        producer = Custom("Image Capture Producer", "./icons/camera.png")
        consumer = Custom("Image Predictor Consumer", "./icons/consumer.png")
        seldon_core = Custom("Seldon Model Server", "./icons/seldon.png")
        minio = Minio("Object Storage")

        with Cluster("Data Streaming"):
            kafka = Kafka("Kafka")

        with Cluster("Model Training & Deployment"):
            github = Github("GitHub")
            seldon = Custom("Seldon Core", "./icons/seldon.png")

    user >> Edge(label="Captures Image") >> producer
    producer >> Edge(label="Streams Images") >> kafka
    kafka >> Edge(label="Pulls Images") >> consumer
    consumer >> Edge(label="Inference Request") >> seldon_core
    seldon_core >> Edge(label="Stores Results") >> minio
    minio >> Edge(label="Displays Results") >> user

    github >> Edge(label="Tracks Model") >> seldon
    seldon >> Edge(label="Deploys Model") >> seldon_core

    grafana = Grafana("Visualization Dashboard")
    minio >> Edge(label="Updates Dashboard") >> grafana