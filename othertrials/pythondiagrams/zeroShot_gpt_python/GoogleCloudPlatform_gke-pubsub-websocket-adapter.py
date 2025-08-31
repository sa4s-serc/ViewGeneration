from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom

with Diagram("Software Architecture", show=True, direction="LR"):
    # Define the components
    component1 = Custom("Component 1", "./icons/component.png")
    component2 = Custom("Component 2", "./icons/component.png")
    component3 = Custom("Component 3", "./icons/component.png")
    
    # Define the connectors
    component1 >> Edge(label="REST API", color="blue") >> component2
    component2 << Edge(label="Function Call", color="red") << component3
    
    # Define a subsystem cluster
    with Cluster("Subsystem"):
        sub_component1 = Custom("Sub Component 1", "./icons/component.png")
        sub_component2 = Custom("Sub Component 2", "./icons/component.png")
        
        sub_component1 >> Edge(label="Message Queue", color="green") >> sub_component2
    
    # Connect subsystem with main components
    component2 >> Edge(label="Data Flow", style="dashed") >> sub_component1
    sub_component2 >> Edge(label="Control Signal", style="dotted") >> component3