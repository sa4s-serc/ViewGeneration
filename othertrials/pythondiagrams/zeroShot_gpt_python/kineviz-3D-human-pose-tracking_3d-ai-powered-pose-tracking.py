from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom

# Metadata extracted
view_details = {
    "summary": "A microservices architecture for an e-commerce platform, focusing on scalability and maintainability.",
    "Concern": "Scalability and Maintainability",
    "Behavior": "Services interact through REST APIs",
    "Granularity": "Component Level",
    "Components Nature": "Services, APIs",
    "Connectors Nature": "REST APIs",
    "QAs": "Scalability, Fault Tolerance",
    "Architecture Scope": "Entire System",
    "Architectural Notation": "Icons and Arrows",
    "Architectural Styles": "Microservices",
    "Shapes": "Rectangles",
    "Colored?": "Yes",
    "Connectors Direction": "Unidirectional",
    "Legend?": "Yes",
    "Nested Components?": "No",
    "Explicit Ports/Interfaces?": "Yes",
    "Explicit Connectors?": "Yes"
}

# Create the diagram
with Diagram("E-commerce Platform Architecture", show=False, direction="TB"):
    with Cluster("Microservices"):
        user_service = Custom("User Service", "./icons/user_service.png")
        product_service = Custom("Product Service", "./icons/product_service.png")
        order_service = Custom("Order Service", "./icons/order_service.png")
        payment_service = Custom("Payment Service", "./icons/payment_service.png")

    # Adding REST API connections with explicit connectors
    user_service >> Edge(label="REST API") >> product_service
    user_service >> Edge(label="REST API") >> order_service
    order_service >> Edge(label="REST API") >> payment_service
    product_service >> Edge(label="REST API") >> order_service

    # Legend
    legend = Custom("Legend", "./icons/legend.png")
    legend - Edge(style="dashed") - user_service