from diagrams import Diagram, Cluster
from diagrams.azure.compute import AppServices
from diagrams.azure.database import SQLDatabases, CosmosDb, CacheForRedis
from diagrams.azure.security import KeyVaults
from diagrams.azure.identity import ActiveDirectory
from diagrams.azure.web import APIConnections

def create_books_store_architecture():
    with Diagram("Books Store Architecture", show=False):
        with Cluster("Frontend"):
            web = AppServices("Blazor WebAssembly")

        with Cluster("Backend"):
            api = APIConnections("ASP.NET Core API")
            auth = ActiveDirectory("Auth0")
            vault = KeyVaults("Key Vault")

        with Cluster("Data Layer"):
            sql = SQLDatabases("SQL Server")
            cache = CacheForRedis("Redis Cache")

        # Frontend to Backend
        web >> api

        # API Authentication
        api >> auth

        # API to Data Stores
        api >> sql
        api >> cache

        # Secrets Management
        api >> vault

if __name__ == "__main__":
    create_books_store_architecture()