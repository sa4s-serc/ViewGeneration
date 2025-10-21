from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.onprem.compute import Server

with Diagram("NVMe SSD Automation Test Framework", show=False, direction="TB"):
    nvme_ioctl = Custom("NVMe IOCTL Library", "./icons/c_library.png")
    common_lib = Custom("Common Library", "./icons/python_lib.png")
    test_cases = Custom("Test Cases", "./icons/tests.png")
    driver = Custom("Driver", "./icons/python_lib.png")
    dynamic_lib = Custom("Dynamic Library", "./icons/c_library.png")
    logic_layer = Custom("Logic Layer", "./icons/python_lib.png")
    data_structures = Custom("Data Structures", "./icons/python_lib.png")
    buffer_management = Custom("Buffer Management", "./icons/python_lib.png")

    with Cluster("Layered Architecture"):
        with Cluster("Driver Layer"):
            dynamic_lib - Edge(label="C Interface") - driver

        with Cluster("Logic Layer"):
            driver - Edge(label="Python Wrapper") - logic_layer
            logic_layer >> Edge(label="Data Transfer", style="dashed") >> data_structures

        with Cluster("Common Library"):
            logic_layer >> Edge(label="High-Level Interface") >> common_lib
            common_lib >> Edge(label="Memory Management") >> buffer_management

        with Cluster("Test Layer"):
            common_lib >> Edge(label="Test Interface") >> test_cases

    dynamic_lib << Edge(label="Build Script") << nvme_ioctl