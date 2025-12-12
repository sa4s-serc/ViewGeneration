from diagrams import Diagram, Cluster
from diagrams.gcp.analytics import BigQuery, Dataflow, PubSub
from diagrams.gcp.ml import AIPlatform
from diagrams.gcp.compute import KubernetesEngine
from diagrams.gcp.storage import Storage
from diagrams.gcp.network import LoadBalancing
from diagrams.gcp.database import Datastore
from diagrams.onprem.workflow import Kubeflow
from diagrams.onprem.container import Docker
from diagrams.programming.framework import Flask
from diagrams.gcp.api import Endpoints

with Diagram("Retail Analytics Architecture", show=False, direction="TB"):
    with Cluster("Data Sources"):
        data_sources = [Storage("Cloud Storage"),
                       BigQuery("BigQuery Data")]
    
    with Cluster("Data Processing"):
        with Cluster("Batch Processing"):
            dataflow = Dataflow("Dataflow")
        
        with Cluster("Stream Processing"):
            pubsub = PubSub("Pub/Sub")
    
    with Cluster("ML Pipeline"):
        with Cluster("Kubeflow Pipelines"):
            kfp = Kubeflow("KFP Orchestration")
        
        with Cluster("Model Training"):
            bqml = BigQuery("BigQuery ML")
            vertex_ai = AIPlatform("Vertex AI")
    
    with Cluster("Model Serving"):
        with Cluster("Real-time Serving"):
            with Cluster("Custom Container"):
                flask_app = Flask("Flask App")
                scann_service = Docker("ScaNN Service")
            
            endpoints = Endpoints("API Endpoints")
            load_balancer = LoadBalancing("Load Balancer")
        
        with Cluster("Batch Serving"):
            bq_serving = BigQuery("BQML Serving")
    
    with Cluster("Storage"):
        model_storage = Storage("Model Artifacts")
        embeddings_storage = Storage("Embeddings")
        metadata_store = Datastore("Item Metadata")
    
    with Cluster("Activation"):
        google_ads = AIPlatform("Google Ads API")
        data_studio = BigQuery("Data Studio")
    
    # Data flow connections
    data_sources >> dataflow
    data_sources >> pubsub
    
    dataflow >> bqml
    pubsub >> vertex_ai
    
    bqml >> kfp
    vertex_ai >> kfp
    
    kfp >> model_storage
    kfp >> embeddings_storage
    
    model_storage >> flask_app
    embeddings_storage >> scann_service
    metadata_store >> scann_service
    
    flask_app >> endpoints
    scann_service >> endpoints
    endpoints >> load_balancer
    
    bqml >> bq_serving
    
    bq_serving >> google_ads
    bq_serving >> data_studio
    load_balancer >> google_ads