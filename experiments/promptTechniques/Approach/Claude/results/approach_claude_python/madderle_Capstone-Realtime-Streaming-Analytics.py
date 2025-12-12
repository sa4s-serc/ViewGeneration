from diagrams import Diagram, Cluster
from diagrams.aws.analytics import Kinesis
from diagrams.aws.compute import Lambda
from diagrams.aws.database import DynamodbTable
from diagrams.aws.storage import S3
from diagrams.aws.ml import SagemakerModel
from diagrams.saas.social import Twitter
from diagrams.aws.integration import SNS
from diagrams.aws.database import ElasticacheForRedis
from diagrams.aws.compute import EC2

with Diagram("Real-Time Stock Price Prediction Architecture", show=False):
    with Cluster("Data Collection"):
        twitter = Twitter("Twitter API")
        stock = EC2("Stock Data Service")
        stream = Kinesis("Data Streaming")
        
    with Cluster("Data Processing"):
        process = Lambda("Processing Function")
        cache = ElasticacheForRedis("Redis Cache")
        store = DynamodbTable("MongoDB")
        
    with Cluster("Analysis"):
        model = SagemakerModel("ML Model")
        storage = S3("Model Storage")
        notify = SNS("Notifications")

    twitter >> stream
    stock >> stream
    stream >> process
    process >> cache
    process >> store
    store >> model
    model >> storage
    model >> notify