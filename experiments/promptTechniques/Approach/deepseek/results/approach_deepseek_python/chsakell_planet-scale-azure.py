from diagrams import Diagram, Cluster
from diagrams.azure.compute import AppServices, FunctionApps
from diagrams.azure.database import CosmosDb, SQLDatabases, CacheForRedis
from diagrams.azure.integration import ServiceBus, APIManagement
from diagrams.azure.network import CDNProfiles, TrafficManagerProfiles, FrontDoors
from diagrams.azure.identity import ActiveDirectory
from diagrams.azure.storage import DataLakeStorage
from diagrams.azure.analytics import AnalysisServices
from diagrams.programming.framework import Angular, DotNet

with Diagram("Planet-Scale Online Store Architecture", show=False, direction="TB"):
    with Cluster("Global Infrastructure"):
        traffic_manager = TrafficManagerProfiles("Azure Traffic Manager")
        cdn = CDNProfiles("Azure CDN")
        
        with Cluster("Primary Region"):
            with Cluster("Web Tier"):
                front_door = FrontDoors("Azure Front Door")
                web_app = AppServices("ASP.NET Core Web App")
                angular_app = Angular("Angular Client")
                
            with Cluster("Application Tier"):
                api_management = APIManagement("API Management")
                
                with Cluster("Microservices"):
                    product_service = AppServices("Product Service")
                    cart_service = AppServices("Cart Service")
                    order_service = AppServices("Order Service")
                    auth_service = AppServices("Auth Service")
                    forum_service = AppServices("Forum Service")
                    search_service = AppServices("Search Service")
                
                service_bus = ServiceBus("Azure Service Bus")
                web_jobs = FunctionApps("WebJobs")
                
            with Cluster("Data Tier"):
                sql_db = SQLDatabases("Azure SQL Server")
                cosmos_db = CosmosDb("Cosmos DB")
                redis_cache = CacheForRedis("Redis Cache")
                azure_search = AnalysisServices("Azure Search")
                data_lake = DataLakeStorage("Data Lake Storage")
                
        with Cluster("Secondary Region"):
            with Cluster("DR Site"):
                dr_web_app = AppServices("DR Web App")
                dr_sql_db = SQLDatabases("DR SQL Server")
                dr_cosmos_db = CosmosDb("DR Cosmos DB")
    
    with Cluster("Identity & Security"):
        active_directory = ActiveDirectory("Azure AD")
    
    # Global traffic flow
    traffic_manager >> cdn
    cdn >> front_door
    
    # Primary region flow
    front_door >> web_app
    web_app >> angular_app
    web_app >> api_management
    
    # Microservices communication
    api_management >> product_service
    api_management >> cart_service
    api_management >> order_service
    api_management >> auth_service
    api_management >> forum_service
    api_management >> search_service
    
    # Data access patterns
    product_service >> cosmos_db
    cart_service >> redis_cache
    order_service >> sql_db
    order_service >> service_bus
    service_bus >> web_jobs
    web_jobs >> sql_db
    auth_service >> active_directory
    forum_service >> sql_db
    search_service >> azure_search
    azure_search >> data_lake
    
    # Data replication
    sql_db >> dr_sql_db
    cosmos_db >> dr_cosmos_db
    web_app >> dr_web_app