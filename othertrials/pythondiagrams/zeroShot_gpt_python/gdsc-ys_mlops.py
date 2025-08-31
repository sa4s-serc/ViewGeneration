from diagrams import Diagram, Cluster, Edge
from diagrams.generic.blank import Blank

with Diagram("Architectural View Diagram", show=True):
    # Define components
    component_a = Blank("Component A")
    component_b = Blank("Component B")
    component_c = Blank("Component C")

    # Define relationships
    component_a >> Edge(label="Connector AB", color="blue", style="dashed") >> component_b
    component_b >> Edge(label="Connector BC", color="red", style="solid") >> component_c

    # Define nested components if any
    with Cluster("Nested Component"):
        nested_component_1 = Blank("Nested Component 1")
        nested_component_2 = Blank("Nested Component 2")

        nested_component_1 >> Edge(label="Nested Connector", color="green") >> nested_component_2

    # Add legend if required
    legend = Blank("Legend: Blue - Dashed, Red - Solid, Green - Nested")