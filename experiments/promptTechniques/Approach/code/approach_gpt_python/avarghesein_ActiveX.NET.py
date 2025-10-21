from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom

with Diagram("ActiveX.NET Framework Architecture", direction="LR"):
    with Cluster("ActiveX.NET Framework"):
        server = Custom("ActiveX.NET.Server", "./server.png")
        plugin = Custom("ActiveX.NET.Plugin", "./plugin.png")
        common = Custom("ActiveX.NET.Common", "./common.png")
        
        with Cluster("Key Components"):
            server_context = Custom("ActiveXServerContext", "./context.png")
            servers = Custom("ActiveXServers", "./servers.png")
            ax_base = Custom("ActiveXServerBase", "./base.png")
            ax_mta_base = Custom("ActiveXServerMTABase", "./mta_base.png")
            ax_control_base = Custom("ActiveXServerControlBase", "./control_base.png")
            ax_attr = Custom("ActiveXServerAttribute", "./attr.png")
            default_factory = Custom("DefaultActiveXFactory", "./factory.png")
        
        server >> Edge(label="hosts and manages") >> server_context
        server_context >> Edge(label="manages") >> servers
        servers >> Edge(label="discovers and manages via MEF") >> Custom("IActiveXServer", "./interface.png")
        
        plugin >> Edge(label="provides sample COM object") >> Custom("CoClass", "./coclass.png")
        
        common >> Edge(label="provides base classes and interfaces") >> [ax_base, ax_mta_base, ax_control_base, ax_attr]

        with Cluster("Design Patterns"):
            plugin_pattern = Custom("Plugin", "./plugin_pattern.png")
            di_pattern = Custom("Dependency Injection", "./di_pattern.png")
            factory_pattern = Custom("Factory", "./factory_pattern.png")
            template_method_pattern = Custom("Template Method", "./template_method_pattern.png")
        
        server >> Edge(label="implements") >> [plugin_pattern, di_pattern, factory_pattern, template_method_pattern]