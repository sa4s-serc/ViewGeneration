from diagrams import Diagram
from diagrams.azure.compute import AppServices, FunctionApps
from diagrams.azure.identity import ADIdentityProtection, ADB2C
from diagrams.azure.database import SQLServers, CosmosDb
from diagrams.azure.integration import ServiceBus, LogicApps
from diagrams.azure.storage import BlobStorage, QueuesStorage
from diagrams.azure.network import TrafficManagerProfiles, CDNProfiles
from diagrams.azure.analytics import AnalysisServices

with Diagram("Planet-Scale Online Store Architecture", show=False):
    user = ADIdentityProtection("User Authentication")
    identity_service = ADB2C("Azure AD B2C")
    
    traffic_manager = TrafficManagerProfiles("Azure Traffic Manager")
    cdn = CDNProfiles("Azure CDN")

    product_catalog = CosmosDb("Product Catalog")
    order_db = SQLServers("Order DB")
    cache = QueuesStorage("Redis Cache")
    service_bus = ServiceBus("Azure Service Bus")
    blob_storage = BlobStorage("Blob Storage")
    logic_app = LogicApps("Order Processing Logic App")
    function_app = FunctionApps("Background Processing")
    
    app_service = AppServices("Web App")
    
    user >> identity_service >> traffic_manager
    traffic_manager >> cdn >> app_service
    app_service >> [product_catalog, order_db, cache]
    app_service >> service_bus >> logic_app >> function_app
    function_app >> blob_storage
    logic_app >> AnalysisServices("Data Analytics")