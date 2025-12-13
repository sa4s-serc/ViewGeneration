from diagrams import Diagram, Cluster
from diagrams.aws.analytics import Kinesis, Analytics
from diagrams.aws.compute import Lambda 
from diagrams.aws.storage import S3
from diagrams.aws.database import Database
from diagrams.aws.integration import SNS
from diagrams.aws.network import APIGateway
from diagrams.aws.management import Cloudwatch

with Diagram("Serverless Traffic Analysis Architecture", show=False):
    
    with Cluster("Data Ingestion & Transformation"):
        xml_retriever = Lambda("XML Data Retriever")
        xml_to_json = Lambda("XML to JSON")
        data_publisher = Lambda("Data Publisher")
        
    with Cluster("Storage"):
        s3_xml = S3("XML Bucket")
        s3_json = S3("JSON Bucket") 
        s3_analytics = S3("Analytics Bucket")
        
    with Cluster("Stream Processing"):
        kinesis_stream = Kinesis("Traffic Data Stream")
        kinesis_analytics = Analytics("Real-time Analytics")
        kinesis_delivery = Kinesis("Data Delivery Stream")
        
    with Cluster("Data Storage & API"):
        dynamodb_analytics = Database("Analytics Table")
        dynamodb_alerts = Database("Alerts Table")
        api = APIGateway("REST API")
        
    with Cluster("Notifications"):
        alert_processor = Lambda("Alert Processor")
        notifications = SNS("Notifications")
        
    # Monitoring
    monitoring = Cloudwatch("Monitoring")
        
    # Data flow
    xml_retriever >> s3_xml >> xml_to_json >> s3_json
    s3_json >> data_publisher >> kinesis_stream
    
    kinesis_stream >> kinesis_analytics
    kinesis_analytics >> [kinesis_delivery, alert_processor]
    
    kinesis_delivery >> s3_analytics
    kinesis_delivery >> dynamodb_analytics
    
    alert_processor >> dynamodb_alerts
    alert_processor >> notifications
    
    [dynamodb_analytics, dynamodb_alerts] >> api
    
    # Monitoring connections
    monitoring >> [xml_retriever, xml_to_json, data_publisher, 
                  kinesis_stream, kinesis_analytics, kinesis_delivery,
                  alert_processor]