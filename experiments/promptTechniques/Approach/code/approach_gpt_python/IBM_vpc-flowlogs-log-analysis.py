from diagrams import Diagram, Cluster, Edge
from diagrams.ibm.cloud.devtools import CodeEngine
from diagrams.ibm.storage import ObjectStorage
from diagrams.ibm.security import LogAnalysis
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server

with Diagram("Serverless Flow Log Processing Architecture", show=False):
    user = User("Developer")

    with Cluster("IBM Cloud"):
        function = CodeEngine("Serverless Function")
        cos_source = ObjectStorage("COS Source Bucket")
        cos_archive = ObjectStorage("COS Archive Bucket")
        log_analysis = LogAnalysis("IBM Log Analysis")

    with Cluster("Local Development"):
        local_handler = Server("local-handler.js")
        http_endpoint = Server("index.js")

    # Connections
    user >> Edge(label="Invoke HTTP") >> http_endpoint
    user >> Edge(label="Simulate Trigger") >> local_handler

    http_endpoint >> Edge(label="Invoke Handler") >> function
    local_handler >> Edge(label="Invoke Handler") >> function

    cos_source >> Edge(label="COS Trigger") >> function
    function >> Edge(label="Retrieve, Decompress, Parse") >> cos_source
    function >> Edge(label="Transform, Forward") >> log_analysis
    function >> Edge(label="Copy to Archive") >> cos_archive

    # Style annotations
    Edge(color="darkgreen", style="dotted")(cos_source, function)
    Edge(color="blue", style="bold")(function, log_analysis)
    Edge(color="red", style="dashed")(function, cos_archive)