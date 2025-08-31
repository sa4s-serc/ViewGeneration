from diagrams import Diagram, Cluster, Edge
from diagrams.generic.blank import Blank
from diagrams.programming.language import Python
from diagrams.onprem.compute import Server

with Diagram("Architecture Diagram", show=False):
    qa = "Scalability"
    
    with Cluster("System Level"):
        component1 = Python("Service A")
        component2 = Python("Service B")
        
        with Cluster("Database Layer"):
            database = Server("Database")
        
        if "Nested Components?" == "Yes":
            with Cluster("Nested Component"):
                nested_service = Python("Nested Service")
                component1 >> nested_service
    
    component1 >> Edge(label="REST API", color="blue") >> component2
    component2 >> Edge(label="DB Call", color="green") >> database

    if "Legend?" == "Yes":
        legend = Blank("This diagram shows the system architecture with components and connectors.")
    
    if "Explicit Ports/Interfaces?" == "Yes":
        component1_port = Blank("Port 1")
        component1_port >> component1
    
    if "Explicit Connectors?" == "Yes":
        explicit_connector = Edge(label="Explicit Connector", style="dashed")
        component1 >> explicit_connector >> component2