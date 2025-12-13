from diagrams import Diagram, Cluster
from diagrams.azure.compute import VM, ContainerInstances, FunctionApps
from diagrams.azure.database import CosmosDb, BlobStorage
from diagrams.azure.network import VirtualNetworks, LoadBalancers
from diagrams.azure.identity import ActiveDirectory
from diagrams.azure.monitor import Monitor
from diagrams.azure.web import AppServices
from diagrams.azure.integration import APIManagement
from diagrams.azure.security import KeyVaults
from diagrams.azure.migration import DatabaseMigrationServices
from diagrams.azure.analytics import DataLakeAnalytics
from diagrams.azure.storage import DataLakeStorage
from diagrams.azure.devops import ApplicationInsights
from diagrams.onprem.compute import Server

with Diagram("CloudLabs Azure Architecture", show=False, direction="TB"):
    with Cluster("On-Premises Environment"):
        onprem_servers = [Server("Hyper-V VM1"), Server("Hyper-V VM2")]
        onprem_ad = ActiveDirectory("Active Directory")
    
    with Cluster("Azure Cloud Environment"):
        with Cluster("Migration Hub"):
            migrate = DatabaseMigrationServices("Azure Migrate")
        
        with Cluster("Virtual Network"):
            with Cluster("Compute Services"):
                vm_iaas = VM("Virtual Machines")
                availability_sets = VM("Availability Sets")
                container_instances = ContainerInstances("Container Instances")
                kubernetes_services = ContainerInstances("Kubernetes Services")
            
            with Cluster("Serverless Modernization"):
                function_apps = FunctionApps("Azure Functions")
                app_services = AppServices("App Services")
                cosmos_db = CosmosDb("Cosmos DB")
                blob_storage = BlobStorage("Blob Storage")
            
            with Cluster("Monitoring & Analytics"):
                monitor = Monitor("Azure Monitor")
                app_insights = ApplicationInsights("Application Insights")
                log_analytics = Monitor("Log Analytics")
                hd_insight = DataLakeAnalytics("Data Lake Analytics")
                data_lake = DataLakeStorage("Data Lake Storage")
        
        with Cluster("Security & Identity"):
            key_vault = KeyVaults("Key Vault")
            azure_ad = ActiveDirectory("Azure AD")
            app_gateway = LoadBalancers("Application Gateway")
        
        api_management = APIManagement("API Management")
    
    onprem_servers >> migrate >> vm_iaas
    onprem_ad >> azure_ad
    vm_iaas >> app_services
    function_apps >> cosmos_db
    function_apps >> blob_storage
    vm_iaas >> monitor
    function_apps >> monitor
    app_services >> monitor
    vm_iaas >> app_insights
    function_apps >> app_insights
    app_services >> app_insights
    monitor >> log_analytics
    app_insights >> log_analytics
    log_analytics >> hd_insight
    hd_insight >> data_lake
    azure_ad >> vm_iaas
    azure_ad >> function_apps
    azure_ad >> app_services
    key_vault >> vm_iaas
    key_vault >> function_apps
    key_vault >> app_services
    app_gateway >> vm_iaas
    app_gateway >> app_services
    api_management >> function_apps
    api_management >> app_services