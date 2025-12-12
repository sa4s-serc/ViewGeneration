from diagrams import Diagram, Cluster
from diagrams.programming.language import Csharp
from diagrams.programming.framework import DotNet
from diagrams.onprem.client import Client
from diagrams.onprem.compute import Server
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.container import Docker

with Diagram("ActiveX.NET Framework Architecture", show=False, direction="TB"):
    client = Client("COM Client")
    
    with Cluster("ActiveX.NET Server"):
        server = Server("ActiveX.NET.Server")
        mef = DotNet("MEF Container")
        context = Csharp("ActiveXServerContext")
        factories = Csharp("DefaultActiveXFactory")
        
        server >> mef
        mef >> context
        context >> factories
    
    with Cluster("Plugin System"):
        common = Csharp("ActiveX.NET.Common")
        plugin1 = Csharp("Sample Plugin")
        plugin2 = Csharp("Custom Plugin")
        
        common >> plugin1
        common >> plugin2
    
    client >> server
    server >> plugin1
    server >> plugin2
    
    threading = DotNet("STA/MTA Threading")
    lifecycle = DotNet("Object Lifecycle Management")
    
    server >> threading
    server >> lifecycle