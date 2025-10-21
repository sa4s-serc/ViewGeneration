from diagrams import Diagram, Cluster
from diagrams.onprem.client import Client
from diagrams.onprem.network import Internet
from diagrams.onprem.compute import Server
from diagrams.onprem.iac import Terraform
from diagrams.onprem.security import Vault
from diagrams.programming.language import NodeJS
from diagrams.programming.flowchart import Database
from diagrams.onprem.analytics import Grafana

with Diagram("Apigee-Based CDS Reference Implementation", show=False, direction="LR"):

    internet = Internet("Internet")
    client = Client("Client App")

    with Cluster("Apigee API Management"):
        api_gateway = Server("API Gateway")
        
        with Cluster("CDS Banking API Proxies"):
            get_products = Server("Get Products")
            get_accounts = Server("Get Accounts")
            get_transactions = Server("Get Transactions")
            discovery_api = Server("Discovery API")
        
        auth_proxy = Vault("OIDC Proxy")
        consent_mgmt = Server("Consent Management Proxy")
        dynamic_client_reg = Server("Dynamic Client Registration")
        shared_flows = Server("Reusable Shared Flows")
        oidc_mock_provider = NodeJS("Mock OIDC Provider")
    
    with Cluster("Additional Solutions"):
        metrics_service = Grafana("Metrics Service")
        admin_apis = Server("Admin APIs")
    
    with Cluster("Configuration"):
        kvm = Database("Key Value Maps")
        openapi_specs = Terraform("OpenAPI Specs")
    
    internet >> client >> api_gateway
    api_gateway >> [get_products, get_accounts, get_transactions, discovery_api]
    api_gateway >> auth_proxy
    api_gateway >> consent_mgmt
    api_gateway >> dynamic_client_reg
    api_gateway >> shared_flows
    api_gateway >> oidc_mock_provider

    auth_proxy >> kvm
    consent_mgmt >> kvm
    dynamic_client_reg >> openapi_specs

    api_gateway >> metrics_service
    api_gateway >> admin_apis