from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS
from diagrams.aws.network import APIGateway
from diagrams.aws.storage import S3
from diagrams.aws.analytics import Kinesis
from diagrams.aws.integration import SQS
from diagrams.aws.ml import Sagemaker
from diagrams.aws.management import Cloudwatch

with Diagram("AWS Microservices Architecture", show=False):
    api_gateway = APIGateway("API Gateway")
    
    with Cluster("Application Layer"):
        with Cluster("User Service"):
            user_lambda = Lambda("User Lambda")
            user_db = RDS("User DB")
            user_lambda >> user_db
        
        with Cluster("Order Service"):
            order_lambda = Lambda("Order Lambda")
            order_db = RDS("Order DB")
            order_lambda >> order_db
        
        with Cluster("Payment Service"):
            payment_lambda = Lambda("Payment Lambda")
            payment_queue = SQS("Payment Queue")
            payment_lambda >> payment_queue
    
    with Cluster("Data Layer"):
        data_stream = Kinesis("Data Stream")
        data_lake = S3("Data Lake")
        data_stream >> data_lake
    
    with Cluster("ML Layer"):
        ml_model = Sagemaker("ML Model")
        training_data = S3("Training Data")
        ml_model << training_data
    
    with Cluster("Monitoring"):
        monitoring = Cloudwatch("CloudWatch")
    
    api_gateway >> user_lambda
    api_gateway >> order_lambda
    api_gateway >> payment_lambda
    user_lambda >> data_stream
    order_lambda >> data_stream
    payment_lambda >> data_stream
    user_lambda >> monitoring
    order_lambda >> monitoring
    payment_lambda >> monitoring
    ml_model >> monitoring