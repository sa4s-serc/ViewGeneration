from diagrams import Diagram, Cluster
from diagrams.azure.compute import ContainerInstances, AppServices, VMLinux
from diagrams.azure.database import CosmosDb, SQLDatabases, CacheForRedis
from diagrams.azure.network import LoadBalancers, CDNProfiles
from diagrams.azure.identity import ActiveDirectory
from diagrams.azure.storage import BlobStorage

with Diagram("Planet-Scale Online Store Architecture", show=False):
    with Cluster("Azure Global Infrastructure"):
        lb = LoadBalancers("Traffic Manager")
        cdn = CDNProfiles("Azure CDN")

        with Cluster("Primary Region"):
            apps = AppServices("Web Apps")
            containers = ContainerInstances("Microservices")
            vm = VMLinux("WebJobs")
            
            db = SQLDatabases("SQL Server")
            cosmos = CosmosDb("Cosmos DB")
            redis = CacheForRedis("Redis Cache")
            storage = BlobStorage("Blob Storage")
            auth = ActiveDirectory("Azure AD B2C")

        # Frontend connections
        lb >> apps
        cdn >> apps

        # Backend connections
        apps >> containers
        containers >> [db, cosmos, redis]
        containers >> storage
        containers >> auth
        
        # Background processing
        containers >> vm
        vm >> [db, cosmos]