from diagrams import Diagram, Cluster
from diagrams.gcp.compute import GKE
from diagrams.firebase.develop import Authentication
from diagrams.gcp.analytics import BigQuery
from diagrams.firebase.develop import Firestore
from diagrams.firebase.develop import Functions
from diagrams.gcp.database import Datastore
from diagrams.gcp.storage import Storage
from diagrams.gcp.network import LoadBalancing
from diagrams.gcp.compute import Run

with Diagram("Tag Engine v3 Architecture", show=False):
    with Cluster("Frontend & API Layer"):
        lb = LoadBalancing("Load Balancer")
        api = Run("Cloud Run API")
        ui = Run("Cloud Run UI")

    with Cluster("Core Services"):
        auth = Authentication("Authentication")
        func = Functions("Cloud Functions")
        store = Firestore("Firestore\nConfigurations")

    with Cluster("Data Processing"):
        bq = BigQuery("BigQuery")
        gcs = Storage("Cloud Storage")
        ds = Datastore("Tag Storage")

    with Cluster("Job Processing"):
        jobs = GKE("Job Processor")

    # Frontend connections
    lb >> [api, ui]

    # Auth and config flow
    api >> auth
    api >> store
    ui >> auth
    ui >> store

    # Data processing flow
    api >> jobs
    jobs >> bq
    jobs >> gcs
    jobs >> ds

    # Function triggers
    store >> func
    func >> jobs