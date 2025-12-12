from diagrams import Diagram, Cluster, Edge
from diagrams.programming.framework import Dotnet
from diagrams.onprem.database import Mssql
from diagrams.saas.identity import Auth0
from diagrams.onprem.inmemory import Redis
from diagrams.programming.framework import Dotnet
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.client import Client
from diagrams.onprem.network import Internet

with Diagram("Books Store Application Architecture", show=False):
    client = Client("User")

    with Cluster("Frontend"):
        blazor = Dotnet("Blazor WebAssembly")

    with Cluster("Backend"):
        api = Dotnet("ASP.NET Core Web API")
        auth = Auth0("Auth0")
        redis = Redis("Redis Cache")
        sql_db = Mssql("SQL Server Database")

    ci_cd = GithubActions("GitHub Actions")
    internet = Internet("Internet")

    client >> internet >> blazor >> api
    api >> auth
    api >> redis
    api >> sql_db
    ci_cd >> api