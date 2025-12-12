from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.queue import Kafka
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDSMysqlInstance
from diagrams.aws.integration import SQS
from diagrams.aws.ml import TensorflowOnAWS
from diagrams.aws.database import DocumentDB
from diagrams.aws.network import APIGateway
from diagrams.aws.storage import S3

with Diagram("Stock Market Prediction Architecture", show=False):
    with Cluster("Data Ingestion"):
        producer = APIGateway("Producer")
        kafka = Kafka("Kafka Stream")
        s3 = S3("CSV Storage")

    with Cluster("Processing Layer"):
        preprocess = Lambda("Pre-processing")
        model = TensorflowOnAWS("LSTM Model")
        consumer = Lambda("ML Consumer")

    with Cluster("Storage Layer"):
        mongodb = DocumentDB("MongoDB")
        mysqldb = RDSMysqlInstance("MySQL")
        queue = SQS("Message Queue")

    # Data flow
    producer >> kafka >> preprocess
    s3 >> preprocess
    preprocess >> model
    model >> consumer
    consumer >> mongodb
    consumer >> mysqldb
    kafka >> queue

    # Training flow
    mongodb >> model
    mysqldb >> model