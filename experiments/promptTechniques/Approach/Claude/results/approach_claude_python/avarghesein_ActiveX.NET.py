from diagrams import Diagram, Cluster
from diagrams.programming.language import Csharp
from diagrams.azure.compute import AppServices
from diagrams.aws.database import DynamodbTable
from diagrams.programming.framework import Dotnet
from diagrams.azure.identity import ActiveDirectory
from diagrams.aws.security import IAM
from diagrams.azure.integration import APIManagement

with Diagram("ActiveX.NET Framework Architecture", show=False):
    with Cluster("ActiveX.NET Framework"):
        with Cluster("Core Components"):
            server = AppServices("ActiveX.NET.Server")
            common = Dotnet("ActiveX.NET.Common")
            plugin = Csharp("ActiveX.NET.Plugin")

        with Cluster("Base Classes"):
            base = Dotnet("ActiveXServerBase")
            mta = Dotnet("ActiveXServerMTABase")
            control = Dotnet("ActiveXServerControlBase")

        with Cluster("Security & Management"):
            auth = ActiveDirectory("COM Registration")
            factory = IAM("DefaultActiveXFactory")
            api = APIManagement("IActiveXServer")

        # Define relationships
        server >> common
        server >> plugin
        common >> [base, mta, control]
        plugin >> base
        auth >> server
        factory >> server
        api >> [base, mta, control]