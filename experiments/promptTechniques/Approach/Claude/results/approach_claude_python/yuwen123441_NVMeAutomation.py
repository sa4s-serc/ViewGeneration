from diagrams import Diagram, Cluster
from diagrams.onprem.database import MySQL
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker
from diagrams.programming.language import Python
from diagrams.onprem.client import Users

with Diagram("NVMe SSD Test Framework Architecture", show=False):
    with Cluster("Test Framework"):
        users = Users("Test Engineers")
        
        with Cluster("Test Cases"):
            test_cases = Python("Test Cases\n(nosetests)")
        
        with Cluster("Framework Core"):
            with Cluster("High Level Interface"):
                logic = Python("Logic Layer\n(Admin/IO Operations)")
            
            with Cluster("Driver Layer"):
                python_driver = Python("Python Driver\n(nvme.py)")
                docker = Docker("C Library Container")
            
            with Cluster("Data Structures"):
                dto = Python("DTOs\n(Command Structures)")
                buffer = Python("Buffer Management")

        with Cluster("Storage Layer"):
            nvme = Server("NVMe SSD Device")

    # Define relationships
    users >> test_cases
    test_cases >> logic
    logic >> python_driver
    logic >> dto
    python_driver >> docker
    python_driver >> buffer
    docker >> nvme
    dto >> python_driver
    buffer >> nvme