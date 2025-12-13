from diagrams import Diagram, Cluster
from diagrams.azure.compute import VM, ContainerInstances, KubernetesServices, AppServices
from diagrams.azure.database import SQLDatabases, CosmosDb, BlobStorage
from diagrams.azure.network import VirtualNetworks, LoadBalancers, ApplicationGateway
from diagrams.azure.identity import ActiveDirectory
from diagrams.azure.security import KeyVaults
from diagrams.azure.web import AppServicePlans
from diagrams.azure.integration import APIManagement
from diagrams.azure.analytics import Databricks
from diagrams.azure.ml import MachineLearningServiceWorkspaces
from diagrams.azure.iot import IotHub
from diagrams.azure.devops import Pipelines
from diagrams.azure.monitor import Monitor
from diagrams.generic.network import Subnet
from diagrams.generic.os import Windows, LinuxGeneral
from diagrams.onprem.network import Internet
with Diagram("AzureStack QuickStart Templates Architecture", show=False, direction="TB"):
    internet = Internet("Internet")
    with Cluster("Azure Stack Environment"):
        with Cluster("Management Layer"):
            ad = ActiveDirectory("Active Directory")
            key_vault = KeyVaults("Key Vault")
            monitor = Monitor("Monitor")
            pipelines = Pipelines("DevOps Pipelines")
        with Cluster("Networking"):
            vnet = VirtualNetworks("Virtual Network")
            with Cluster("Subnets"):
                web_subnet = Subnet("Web Subnet")
                app_subnet = Subnet("App Subnet")
                data_subnet = Subnet("Data Subnet")
            lb = LoadBalancers("Load Balancer")
            app_gateway = ApplicationGateway("App Gateway")
        with Cluster("Compute Layer"):
            with Cluster("Web Tier"):
                web_vm_win = VM("Web VM Windows")
                web_vm_linux = VM("Web VM Linux")
                app_service = AppServices("App Service")
            with Cluster("Application Tier"):
                app_vm = VM("App VM")
                aci = ContainerInstances("Container Instances")
                aks = KubernetesServices("Kubernetes Service")
            with Cluster("Data Tier"):
                sql_db = SQLDatabases("SQL Database")
                cosmos_db = CosmosDb("Cosmos DB")
                blob_storage = BlobStorage("Blob Storage")
        with Cluster("Platform Services"):
            api_mgmt = APIManagement("API Management")
            databricks = Databricks("Databricks")
            ml_workspace = MachineLearningServiceWorkspaces("ML Workspace")
            iot_hub = IotHub("IoT Hub")
    internet >> app_gateway
    app_gateway >> [web_vm_win, web_vm_linux, app_service]
    web_vm_win >> app_vm
    web_vm_linux >> app_vm
    app_service >> app_vm
    app_vm >> [sql_db, cosmos_db, blob_storage]
    aci >> [sql_db, cosmos_db]
    aks >> [sql_db, cosmos_db]
    api_mgmt >> [app_vm, aci, aks]
    databricks >> blob_storage
    ml_workspace >> blob_storage
    iot_hub >> blob_storage
    ad >> [web_vm_win, web_vm_linux, app_vm]
    key_vault >> [web_vm_win, web_vm_linux, app_vm, aci, aks]
    monitor >> [web_vm_win, web_vm_linux, app_vm, aci, aks, sql_db, cosmos_db, blob_storage]
    pipelines >> [web_vm_win, web_vm_linux, app_vm, aci, aks, app_service]