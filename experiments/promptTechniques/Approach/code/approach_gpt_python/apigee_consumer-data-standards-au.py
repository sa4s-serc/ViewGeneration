from diagrams import Cluster, Diagram
from diagrams.gcp.api import Apigee
from diagrams.gcp.compute import AppEngine
from diagrams.gcp.analytics import PubSub
from diagrams.gcp.database import Datastore
from diagrams.onprem.queue import Kafka
from diagrams.onprem.monitoring import Grafana
from diagrams.saas.chat import Slack
from diagrams.elastic.elasticsearch import Kibana
from diagrams.elastic.elasticsearch import Elasticsearch
from diagrams.elastic.elasticsearch import Logstash
from diagrams.elastic.elasticsearch import Beats
from diagrams.firebase.develop import Functions
from diagrams.firebase.develop import Firestore
from diagrams.aws.storage import S3

with Diagram("Apigee-Based CDS Reference Implementation", show=False):
    with Cluster("Apigee Platform"):
        apigee = Apigee("API Gateway")
        
        with Cluster("CDS Banking API Proxies"):
            get_products = Functions("Get Products")
            get_accounts = Functions("Get Accounts")
            get_transactions = Functions("Get Transactions")
            discovery_api = Functions("Discovery API")
        
        with Cluster("Authentication & Authorization"):
            oidc_proxy = Functions("OIDC Proxy")
        
        with Cluster("Consent Management"):
            consent_mgmt = Functions("ConsentMgmtWithKVM Proxy")
        
        with Cluster("Dynamic Client Registration"):
            dynamic_client_reg = Functions("Dynamic Client Registration")
        
        with Cluster("Reusable Artefacts"):
            shared_flows = [
                Functions("Request Header Checking"),
                Functions("Pagination"),
                Functions("Traffic Threshold Application"),
                Functions("JWT Verification"),
                Functions("Request Parameter Validation")
            ]

        with Cluster("Mock OIDC Provider"):
            oidc_mock_provider = Functions("OIDC Mock Provider")
        
        with Cluster("Admin APIs"):
            admin_apis = [
                Functions("Metadata Update"),
                Functions("Get Metrics")
            ]
        
        with Cluster("Metrics Service"):
            metrics_service = [
                AppEngine("Metrics Collection"),
                PubSub("Apigee Analytics"),
                Grafana("Performance Metrics")
            ]
        
    datastore = Datastore("Key Value Maps (KVM)")
    s3 = S3("Mock Data Storage")
    kafka = Kafka("Message Queues")
    elasticsearch = Elasticsearch("Elasticsearch")
    logstash = Logstash("Logstash")
    beats = Beats("Beats")
    kibana = Kibana("Kibana")
    slack = Slack("Slack Notifications")

    apigee >> get_products
    apigee >> get_accounts
    apigee >> get_transactions
    apigee >> discovery_api
    apigee >> oidc_proxy
    apigee >> consent_mgmt
    apigee >> dynamic_client_reg
    apigee >> shared_flows
    apigee >> oidc_mock_provider
    apigee >> admin_apis
    apigee >> metrics_service

    datastore >> consent_mgmt
    s3 >> get_products
    s3 >> get_accounts
    s3 >> get_transactions
    s3 >> discovery_api
    kafka >> metrics_service
    elasticsearch >> logstash >> beats
    logstash >> kibana
    elasticsearch >> kibana
    metrics_service >> slack