from diagrams import Diagram, Cluster
from diagrams.azure.compute import VM
from diagrams.azure.general import Userresource
from diagrams.azure.integration import Functions
from diagrams.azure.management import LogAnalyticsWorkspaces
from diagrams.azure.network import VirtualNetworks
from diagrams.azure.storage import StorageAccounts
from diagrams.azure.monitor import ApplicationInsights
from diagrams.azure.database import CosmosDb
from diagrams.onprem.compute import Server

with Diagram("SpektraSystems_CloudLabs-Azure Architecture", show=False, direction="TB"):
    user = Userresource("User")

    with Cluster("On-Premises Environment"):
        hyperv_vm = Server("Hyper-V VM")

    with Cluster("Azure Cloud Environment"):
        with Cluster("Azure Migrate"):
            migrate_vm = VM("Migrated VM")

        with Cluster("Azure IaaS"):
            azure_vm = VM("Azure VM")
            vnet = VirtualNetworks("Virtual Network")
            azure_vm - vnet

        with Cluster("Serverless App Modernization"):
            function_app = Functions("Azure Functions")
            cosmos_db = CosmosDb("Cosmos DB")
            storage = StorageAccounts("Azure Storage")

            function_app >> cosmos_db
            user >> function_app
            function_app >> storage

        with Cluster("Monitoring and Observability"):
            log_analytics = LogAnalyticsWorkspaces("Log Analytics")
            app_insights = ApplicationInsights("App Insights")

            azure_vm >> log_analytics
            function_app >> app_insights

    user >> hyperv_vm >> migrate_vm
    migrate_vm >> azure_vm