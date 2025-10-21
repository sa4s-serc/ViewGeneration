from diagrams import Diagram, Cluster, Edge
from diagrams.azure.compute import FunctionApps
from diagrams.azure.storage import BlobStorage, TableStorage
from diagrams.azure.identity import ActiveDirectory
from diagrams.azure.general import ResourceGroup
from diagrams.azure.network import APIGateway
from diagrams.azure.devops import Devops
from diagrams.azure.web import AppServiceDomain
from diagrams.onprem.client import Users
from diagrams.onprem.client import Client

with Diagram("UnoCash Architecture", show=False, direction="TB"):
    users = Users("Users")

    with Cluster("Frontend"):
        blazor = Client("Blazor SPA")
        blazor - Edge(label="HTTP/S") - users

    with Cluster("Backend"):
        functions = FunctionApps("Azure Functions")
        api_gateway = APIGateway("Azure API Management")
        ad = ActiveDirectory("Azure AD")
        table_storage = TableStorage("Azure Table Storage")
        blob_storage = BlobStorage("Azure Blob Storage")

        functions >> Edge(label="Secure Access") >> blob_storage
        functions >> Edge(label="Read/Write") >> table_storage
        functions >> Edge(label="Auth") >> ad
        api_gateway >> Edge(label="Route & Policy") >> functions

    with Cluster("Infrastructure"):
        pulumi = Devops("Pulumi")
        resource_group = ResourceGroup("Azure Resource Group")
        dns = AppServiceDomain("DNS")

        pulumi >> resource_group
        resource_group >> [functions, blob_storage, table_storage, api_gateway, ad, dns]

    blazor >> Edge(label="API Calls") >> api_gateway