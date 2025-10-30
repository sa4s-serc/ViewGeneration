from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.analytics import KinesisDataStreams, KinesisDataFirehose, KinesisDataAnalytics
from diagrams.aws.database import Dynamodb
from diagrams.aws.storage import S3
from diagrams.aws.integration import SNS, SQS
from diagrams.saas.chat import Slack
from diagrams.programming.framework import Flask
from diagrams.onprem.analytics import Powerbi

with Diagram("Serverless Data Pipeline - Traffic Analysis", show=False):
    with Cluster("Data Ingestion"):
        ingestion_lambda = Lambda("RetrieveXMLTrafficData")

    with Cluster("Data Transformation"):
        transformation_lambda = Lambda("TransformTrafficDataToJson")

    with Cluster("Data Processing"):
        processing_lambda = Lambda("PublishTrafficData")
        stream_processor_lambda = Lambda("StreamProcessor")

    with Cluster("Real-time Analytics"):
        analytics_app = KinesisDataAnalytics("Analytics SQL")
        kinesis_stream = KinesisDataStreams("Kinesis Stream")
        kinesis_firehose = KinesisDataFirehose("Kinesis Firehose")

    with Cluster("Data Storage"):
        realtime_analytics_table = Dynamodb("RealTimeAnalyticsPerPointTable")
        traffic_alerts_table = Dynamodb("TrafficJamAlertsTable")
        s3_bucket = S3("Traffic Data")

    with Cluster("Alerting & Monitoring"):
        alert_saver_lambda = Lambda("AlertSaver")
        alert_sender_lambda = Lambda("AlertSender")
        sns_alert = SNS("Traffic Alerts")
        slack_alert = Slack("Slack Notification")
        flask_api = Flask("Flask API")

    with Cluster("Data Visualization"):
        powerbi = Powerbi("Power BI")
        current_situation_lambda = Lambda("CurrentSituation")
        current_alerts_lambda = Lambda("CurrentAlerts")

    ingestion_lambda >> s3_bucket
    s3_bucket >> transformation_lambda >> processing_lambda
    processing_lambda >> kinesis_firehose >> s3_bucket
    processing_lambda >> kinesis_stream >> stream_processor_lambda
    stream_processor_lambda >> analytics_app >> realtime_analytics_table
    stream_processor_lambda >> traffic_alerts_table
    traffic_alerts_table >> alert_saver_lambda
    alert_saver_lambda >> alert_sender_lambda
    alert_sender_lambda >> sns_alert >> slack_alert
    alert_sender_lambda >> flask_api
    realtime_analytics_table >> current_situation_lambda >> flask_api
    traffic_alerts_table >> current_alerts_lambda >> flask_api
    s3_bucket >> powerbi