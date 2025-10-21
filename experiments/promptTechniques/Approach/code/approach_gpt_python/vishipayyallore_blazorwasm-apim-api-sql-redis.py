from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.azure.web import AppService
from diagrams.onprem.database import Mssql
from diagrams.onprem.inmemory import Redis
from diagrams.azure.compute import FunctionApp
from diagrams.generic.network import Firewall
from diagrams.azure.identity import B2C
from diagrams.azure.integration import APIManagement

with Diagram("Books Store Application Architecture", show=False):
    client = User("User")

    with Cluster("Client-Side"):
        blazor_ui = AppService("Blazor WebAssembly")

    with Cluster("Server-Side"):
        api_controller = FunctionApp("BooksController")
        business_logic = FunctionApp("BooksBll")
        
        with Cluster("Data Access Layer"):
            sql_repo = FunctionApp("BookRepository")
            cache_repo = FunctionApp("BookCacheRepository")

    with Cluster("Data Storage"):
        sql_db = Mssql("SQL Server")
        redis_cache = Redis("Redis Cache")

    auth = B2C("Auth0")
    api_mgmt = APIManagement("Azure API Gateway")
    ci_cd = FunctionApp("CI/CD (GitHub Actions)")

    client >> blazor_ui >> api_mgmt >> api_controller
    api_controller >> auth
    api_controller >> business_logic
    business_logic >> cache_repo >> redis_cache
    business_logic >> sql_repo >> sql_db
    ci_cd >> sql_db