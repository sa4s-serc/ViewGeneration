from diagrams import Diagram, Cluster
from diagrams.azure.compute import ACR, AKS
from diagrams.azure.identity import ActiveDirectory
from diagrams.azure.network import LoadBalancers, VirtualNetworks, DDOSProtectionPlans
from diagrams.azure.web import AppServices, AppServicePlans
from diagrams.azure.database import SQLDatabases
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.queue import RabbitMQ
from diagrams.onprem.iac import Terraform

with Diagram("AzureStack QuickStart Templates Architecture", show=False):
    with Cluster("Azure Environment"):
        vnet = VirtualNetworks("Virtual Network")
        
        with Cluster("Infrastructure"):
            lb = LoadBalancers("Load Balancer")
            lb - vnet
            
            with Cluster("Compute"):
                k8s = AKS("Kubernetes Cluster")
                acr = ACR("Container Registry")
                k8s - acr
                lb - k8s
            
            with Cluster("Identity"):
                ad = ActiveDirectory("Active Directory")
                ad - k8s
        
        with Cluster("Application Layer"):
            app_service = AppServices("App Services")
            app_plan = AppServicePlans("App Service Plans")
            app_service - app_plan
            k8s - app_service
        
        db = SQLDatabases("SQL Database")
        vnet - db
        
        ddos = DDOSProtectionPlans("DDoS Protection")
        ddos - vnet

    with Cluster("On-premises"):
        prometheus = Prometheus("Monitoring")
        rabbitmq = RabbitMQ("Message Queue")
        terraform = Terraform("IaC")
        
        prometheus >> rabbitmq
        terraform >> prometheus
        terraform >> rabbitmq