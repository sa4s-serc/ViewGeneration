from diagrams import Diagram, Cluster, Edge
from diagrams.generic.blank import Blank

with Diagram("Architecture Overview", show=True, direction="LR"):
    with Cluster("System Level"):
        service1 = Blank("Service 1")
        service2 = Blank("Service 2")

    with Cluster("Subsystem Level"):
        with Cluster("Module A"):
            component1 = Blank("Component 1")
            component2 = Blank("Component 2")
        
        with Cluster("Module B"):
            component3 = Blank("Component 3")
            component4 = Blank("Component 4")

    service1 >> Edge(label="REST API", color="blue") >> component1
    component2 >> Edge(label="Function Call", color="green") >> component3
    component3 >> Edge(label="Message Queue", color="red") >> service2
    component4 >> Edge(label="Database Access", color="orange") >> service1