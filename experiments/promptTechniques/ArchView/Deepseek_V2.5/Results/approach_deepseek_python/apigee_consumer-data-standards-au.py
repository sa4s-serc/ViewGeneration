from diagrams import Diagram
from diagrams.gcp.api import Apigee
from diagrams.gcp.compute import AppEngine
from diagrams.gcp.database import Datastore
from diagrams.gcp.security import IAP
from diagrams.gcp.analytics import Dataflow
from diagrams.gcp.network import LoadBalancing
from diagrams.onprem.client import User
from diagrams.onprem.network import Internet
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.workflow import Airflow

with Diagram("Apigee CDS Reference Implementation", show=False, direction="TB"):
    internet = Internet("Internet")
    user = User("End User")
    
    with Diagram("Apigee Platform"):
        apigee = Apigee("Apigee Gateway")
        
        with Diagram("API Proxies"):
            banking_apis = Apigee("CDS Banking APIs")
            oidc_proxy = Apigee("OIDC Proxy")
            consent_proxy = Apigee("Consent Management")
            admin_apis = Apigee("Admin APIs")
            
        with Diagram("Shared Flows"):
            shared_flows = Apigee("Reusable Flows")
    
    with Diagram("External Services"):
        mock_oidc = AppEngine("Mock OIDC Provider")
        metrics_service = AppEngine("Metrics Service")
        kvm = Datastore("Key Value Maps")
        
    with Diagram("Data Stores"):
        postgresql = PostgreSQL("Consent Database")
        redis = Redis("Cache")
    
    user >> internet >> apigee
    apigee >> banking_apis
    apigee >> oidc_proxy
    apigee >> consent_proxy
    apigee >> admin_apis
    apigee >> shared_flows
    
    oidc_proxy >> mock_oidc
    consent_proxy >> kvm
    consent_proxy >> postgresql
    consent_proxy >> redis
    admin_apis >> metrics_service
    
    banking_apis - shared_flows
    oidc_proxy - shared_flows
    consent_proxy - shared_flows