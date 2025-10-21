from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.onprem.compute import Server
from diagrams.onprem.client import Client
from diagrams.onprem.container import Docker

with Diagram("Tengine Lite Architecture", show=True, direction="TB"):

    with Cluster("Core Functionalities"):
        model_conversion = Custom("Model Conversion", "./icons/conversion.png")
        inference_engine = Custom("Inference Engine", "./icons/inference.png")
        operator_library = Custom("Operator Library", "./icons/operators.png")
        testing_framework = Custom("Testing Framework", "./icons/testing.png")

    with Cluster("Key Components"):
        device_abstraction_layer = Custom("Device Abstraction Layer", "./icons/device.png")
        graph_representation = Custom("Graph Representation", "./icons/graph.png")
        operator_prototypes = Custom("Operator Prototypes", "./icons/operator_prototypes.png")
        memory_management = Custom("Memory Management", "./icons/memory.png")
        shader_management = Custom("Shader Management", "./icons/shader.png")
        online_reporting = Custom("Online Reporting", "./icons/reporting.png")
        python_bindings = Custom("Python Bindings", "./icons/python.png")

    hardware_backends = [Server("CPU"), Server("GPU"), Server("NPU")]

    model_conversion >> inference_engine
    inference_engine >> operator_library
    operator_library >> testing_framework

    device_abstraction_layer >> hardware_backends
    graph_representation >> model_conversion
    operator_prototypes >> operator_library
    memory_management >> [Server("Vulkan"), Server("OpenCL")]
    shader_management >> Server("Vulkan")
    online_reporting >> inference_engine
    python_bindings >> inference_engine

    for backend in hardware_backends:
        inference_engine >> Edge(color="blue") >> backend