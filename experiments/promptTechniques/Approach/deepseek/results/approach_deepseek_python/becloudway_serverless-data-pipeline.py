from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.storage import S3
from diagrams.aws.analytics import KinesisDataStreams, KinesisDataFirehose, KinesisDataAnalytics
from diagrams.aws.database import Dynamodb
from diagrams.aws.integration import SQS
from diagrams.aws.network import APIGateway
from diagrams.onprem.analytics import Powerbi
from diagrams.saas.chat import Slack
from diagrams.programming.framework import Flask

with Diagram("Serverless Data Pipeline - Traffic Analysis", show=False, direction="TB"):
    external_api = Flask("Flanders Traffic API")
    
    with Cluster("Data Ingestion & Transformation"):
        s3_xml = S3("S3 XML Storage")
        s3_json = S3("S3 JSON Storage")
        retrieve_xml = Lambda("RetrieveXMLTrafficData")
        transform_json = Lambda("TransformTrafficDataToJson")
        publish_data = Lambda("PublishTrafficData")
        
        external_api >> retrieve_xml >> s3_xml
        s3_xml >> transform_json >> s3_json
        s3_json >> publish_data

    with Cluster("Real-time Processing"):
        kinesis_stream = KinesisDataStreams("Kinesis Stream")
        kinesis_firehose = KinesisDataFirehose("Kinesis Firehose")
        kinesis_analytics = KinesisDataAnalytics("Kinesis Data Analytics")
        stream_processor = Lambda("StreamProcessor")
        
        publish_data >> kinesis_stream
        kinesis_stream >> stream_processor
        kinesis_stream >> kinesis_analytics
        kinesis_analytics >> kinesis_firehose

    with Cluster("Data Storage"):
        s3_analytics = S3("S3 Analytics Storage")
        dynamodb_analytics = Dynamodb("RealTimeAnalyticsPerPointTable")
        dynamodb_alerts = Dynamodb("TrafficJamAlertsTable")
        
        kinesis_firehose >> s3_analytics
        kinesis_analytics >> dynamodb_analytics

    with Cluster("Alerting & Notification"):
        alert_saver = Lambda("AlertSaver")
        alert_sender = Lambda("AlertSender")
        slack = Slack("Slack")
        
        dynamodb_alerts >> alert_saver
        dynamodb_alerts >> alert_sender >> slack

    with Cluster("Data Forwarding & APIs"):
        powerbi = Powerbi("Power BI")
        current_situation = Lambda("CurrentSituation")
        current_alerts = Lambda("CurrentAlerts")
        api_gateway = APIGateway("API Gateway")
        powerbi_forwarder = Lambda("PowerBiForwarder")
        
        kinesis_stream >> powerbi_forwarder >> powerbi
        current_situation >> api_gateway
        current_alerts >> api_gateway

    with Cluster("Error Handling"):
        sqs_dlq = SQS("Dead Letter Queue")
        
        stream_processor >> sqs_dlq
        powerbi_forwarder >> sqs_dlq
        alert_sender >> sqs_dlq

    # Connect components with appropriate edges
    stream_processor >> kinesis_analytics
    kinesis_analytics >> dynamodb_alerts
    dynamodb_analytics >> current_situation
    dynamodb_alerts >> current_alerts