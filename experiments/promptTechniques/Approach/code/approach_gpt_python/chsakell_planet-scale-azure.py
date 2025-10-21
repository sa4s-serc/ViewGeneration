from diagrams import Diagram, Cluster
from diagrams.azure.network import TrafficManagerProfiles
from diagrams.azure.web import AppServices
from diagrams.azure.database import SQLDatabases, CosmosDb
from diagrams.azure.storage import BlobStorage
from diagrams.azure.compute import AppServices as WebApps
from diagrams.azure.search import SearchServices
from diagrams.azure.general import ResourceGroups
from diagrams.azure.identity import ActiveDirectoryB2C
from diagrams.azure.integration import ServiceBus
from diagrams.azure.management import ApplicationInsights
from diagrams.azure.web import CdnProfiles
from diagrams.azure.compute import Functions
from diagrams.azure.cache import RedisCaches

with Diagram("Planet-Scale Online Store Application on Azure", direction="TB", outformat="png"):

    # Azure Traffic Manager for intelligent routing
    traffic_manager = TrafficManagerProfiles("Azure Traffic Manager")

    # CDN for static content
    cdn = CdnProfiles("Azure CDN")

    # Azure Web App for hosting application
    with Cluster("Web App Cluster"):
        web_app = WebApps("Online Store Web App")

    # Azure SQL Database
    sql_db = SQLDatabases("Azure SQL Database")

    # Cosmos DB for NoSQL data
    cosmos_db = CosmosDb("Azure Cosmos DB")

    # Blob Storage for static files
    blob_storage = BlobStorage("Azure Blob Storage")

    # Azure Redis Cache
    redis_cache = RedisCaches("Azure Redis Cache")

    # Azure Service Bus for messaging
    service_bus = ServiceBus("Azure Service Bus")

    # Azure Search for full-text search
    azure_search = SearchServices("Azure Search")

    # Azure Active Directory B2C for identity management
    active_directory = ActiveDirectoryB2C("Azure AD B2C")

    # Azure Functions for background tasks
    webjobs = Functions("Azure WebJobs")

    # Application Insights for monitoring
    app_insights = ApplicationInsights("Azure Application Insights")

    # Diagram connections
    traffic_manager >> web_app
    traffic_manager >> cdn

    web_app >> sql_db
    web_app >> cosmos_db
    web_app >> blob_storage
    web_app >> redis_cache
    web_app >> service_bus
    web_app >> azure_search
    web_app >> active_directory

    service_bus >> webjobs

    web_app >> app_insights