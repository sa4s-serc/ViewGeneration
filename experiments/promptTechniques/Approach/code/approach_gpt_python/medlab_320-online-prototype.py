from diagrams import Diagram, Cluster
from diagrams.azure.web import AppServices
from diagrams.azure.devops import Repos
from diagrams.azure.database import SQLDatabases
from diagrams.azure.identity import ActiveDirectory
from diagrams.onprem.client import Users
from diagrams.onprem.network import Nginx
from diagrams.onprem.compute import Server

with Diagram("Educational Web Application Architecture", show=False):
    user = Users("User")

    with Cluster("Frontend"):
        react_app = AppServices("React App")
        user >> react_app

    with Cluster("Backend"):
        nginx = Nginx("Nginx")
        dotnet_app = Server(".NET Core Backend")

        react_app >> nginx >> dotnet_app

        with Cluster("Data & Auth"):
            database = SQLDatabases("SQL Database")
            auth = ActiveDirectory("OAuth/OIDC")

        dotnet_app >> database
        dotnet_app >> auth

    with Cluster("System Integration Testing"):
        jest = Repos("Jest")
        puppeteer = Repos("Puppeteer")

        react_app >> jest
        react_app >> puppeteer

    with Cluster("Microservices"):
        auth_service = Server("Auth Service")
        logging_service = Server("Logging Service")
        tracing_service = Server("Tracing Service")

        dotnet_app >> auth_service
        dotnet_app >> logging_service
        dotnet_app >> tracing_service