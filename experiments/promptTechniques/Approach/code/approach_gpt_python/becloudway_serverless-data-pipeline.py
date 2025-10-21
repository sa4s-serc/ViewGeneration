from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import DynamodbTable
from diagrams.aws.integration import SQS
from diagrams.aws.analytics import KinesisDataAnalyticsApplication
from diagrams.aws.kinesis import KinesisDataStreams, KinesisFirehose
from diagrams.aws.storage import SimpleStorageServiceS3Bucket
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IdentityAndAccessManagementIamRole
from diagrams.aws.management import Cloudtrail
from diagrams.onprem.client import User
from diagrams.onprem.monitoring import Prometheus

with Diagram("Serverless Data Pipeline - Traffic Analysis", show=False, direction="TB"):
    user = User("Public API")

    with Cluster("Data Ingestion"):
        retrieve_xml = Lambda("RetrieveXMLTrafficData")
        s3_raw = SimpleStorageServiceS3Bucket("Raw XML Bucket")
        user >> retrieve_xml >> s3_raw

    with Cluster("Data Transformation"):
        transform_json = Lambda("TransformTrafficDataToJson")
        s3_raw >> transform_json
        s3_json = SimpleStorageServiceS3Bucket("JSON Data Bucket")
        transform_json >> s3_json

    with Cluster("Data Streaming"):
        publish_data = Lambda("PublishTrafficData")
        kinesis_stream = KinesisDataStreams("Kinesis Stream")
        s3_json >> publish_data >> kinesis_stream

    with Cluster("Real-time Analytics"):
        kinesis_analytics = KinesisDataAnalyticsApplication("Kinesis Data Analytics")
        kinesis_stream >> kinesis_analytics
        realtime_table = DynamodbTable("RealTimeAnalyticsPerPointTable")

    with Cluster("Data Storage"):
        kinesis_analytics >> realtime_table
        s3_analytics = SimpleStorageServiceS3Bucket("Analytics Data Bucket")
        kinesis_analytics >> s3_analytics

    with Cluster("Alerting"):
        alert_saver = Lambda("AlertSaver")
        alert_sender = Lambda("AlertSender")
        traffic_jam_table = DynamodbTable("TrafficJamAlertsTable")
        alert_saver >> traffic_jam_table
        alert_saver >> alert_sender
        cloudwatch = Cloudwatch("CloudWatch Alert")
        alert_sender >> cloudwatch

    with Cluster("Data Forwarding"):
        power_bi_forwarder = Lambda("PowerBiForwarder")
        kinesis_stream >> power_bi_forwarder

    with Cluster("REST Endpoints"):
        current_situation = Lambda("CurrentSituation")
        current_alerts = Lambda("CurrentAlerts")
        realtime_table >> current_situation
        traffic_jam_table >> current_alerts

    with Cluster("Error Handling"):
        dlq = SQS("Dead-letter Queue")
        publish_data >> dlq
        power_bi_forwarder >> dlq

    with Cluster("Security & Monitoring"):
        iam_role = IdentityAndAccessManagementIamRole("IAM Role")
        cloudtrail = Cloudtrail("CloudTrail")
        prometheus = Prometheus("Prometheus")
        iam_role >> [retrieve_xml, transform_json, publish_data, alert_saver, alert_sender, power_bi_forwarder, current_situation, current_alerts]
        cloudtrail >> prometheus