from diagrams import Diagram, Cluster, Edge
from diagrams.generic.blank import Blank
from diagrams.programming.flowchart import Action, InputOutput, Database

with Diagram("Peekaboo Node-RED Node Set Architecture", show=False, direction="TB"):
    with Cluster("Node-RED Nodes"):
        provider = Action("Provider\n(Pull, Push)")
        inference = Action("Inference\n(Classify, Detect, Extract)")
        filter_node = Action("Filter\n(Select, Noisify, Spoof)")
        network = Action("Network\n(Post)")
        utility = Action("Utility\n(Aggregate, pkbInject, pkbJoin)")

    with Cluster("Dynamic UI Generation"):
        dom_util = Database("dom-util.js")
        json_files = Database("[model].json")

    with Cluster("Service Abstraction"):
        peekaboo_service = Action("PeekabooService")
        async_service = Action("AsyncPeekabooService")

    with Cluster("Sensor Configuration"):
        wifi_config = Action("WiFiConfig")

    state_management = Action("StateIO")
    ui_widget_integration = Action("UI Widget\nIntegration")
    resource_dist = Database("resource-dist.js")
    filter_image = InputOutput("filter-image.js")
    inference_services = InputOutput("inference-services.js")
    buffer_stream = InputOutput("buffer-stream.js")
    noisify_audio = InputOutput("noisify-audio.js")

    provider >> Edge(label="Data Source") >> inference
    inference >> Edge(label="Data Process") >> filter_node
    filter_node >> Edge(label="Data Filter") >> network
    network >> Edge(label="Data Transmission") >> Blank("Cloud Service")

    dom_util >> Edge(label="UI Gen") >> provider
    json_files >> Edge(label="Config") >> dom_util

    peekaboo_service >> Edge(label="Service Call") >> inference
    async_service >> Edge(label="Async Call") >> inference

    wifi_config >> Edge(label="Setup") >> provider
    state_management >> Edge(label="State") >> provider
    ui_widget_integration >> Edge(label="UI Enhance") >> provider

    resource_dist >> Edge(label="Static Assets") >> provider
    filter_image >> Edge(label="Image Process") >> filter_node
    inference_services >> Edge(label="Service Layer") >> inference
    buffer_stream >> Edge(label="Buffer") >> filter_node
    noisify_audio >> Edge(label="Audio Process") >> filter_node