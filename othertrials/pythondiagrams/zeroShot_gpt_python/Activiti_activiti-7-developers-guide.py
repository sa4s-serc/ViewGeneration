from graphviz import Digraph

# Define metadata
view_details = {
    "summary": "This architecture represents a microservices-based e-commerce platform.",
    "Concern": "scalability",
    "Behavior": "Services communicate via REST APIs",
    "Granularity": "system",
    "Components Nature": ["Service", "Database", "API Gateway"],
    "Connectors Nature": ["REST API", "Message Queue"],
    "QAs": ["scalability", "fault tolerance"],
    "Architecture Scope": "entire system",
    "Architectural Notation": "icons and arrows",
    "Architectural Styles": "microservices",
    "Shapes": "box",
    "Colored?": "yes",
    "Connectors Direction": "unidirectional",
    "Legend?": "yes",
    "Nested Components?": "no",
    "Explicit Ports/Interfaces?": "no",
    "Explicit Connectors?": "yes"
}

# Create a new directed graph
dot = Digraph(comment='Microservices-based E-commerce Platform')

# Set graph attributes
dot.attr('node', shape='box', style='filled')

# Define nodes
dot.node('A', 'API Gateway', fillcolor='lightblue')
dot.node('B', 'Auth Service', fillcolor='lightgreen')
dot.node('C', 'Catalog Service', fillcolor='lightpink')
dot.node('D', 'Order Service', fillcolor='lightyellow')
dot.node('E', 'User Database', fillcolor='lightgrey')
dot.node('F', 'Product Database', fillcolor='lightgrey')
dot.node('G', 'Order Database', fillcolor='lightgrey')

# Define edges
dot.edge('A', 'B', label='REST API')
dot.edge('A', 'C', label='REST API')
dot.edge('A', 'D', label='REST API')
dot.edge('B', 'E', label='DB Access', dir='none')
dot.edge('C', 'F', label='DB Access', dir='none')
dot.edge('D', 'G', label='DB Access', dir='none')

# Define legend
dot.node('L1', 'Legend', shape='plaintext')
dot.node('L2', 'Service Node', shape='box', fillcolor='lightgreen')
dot.node('L3', 'Database Node', shape='box', fillcolor='lightgrey')
dot.node('L4', 'API Gateway', shape='box', fillcolor='lightblue')

dot.edge('L1', 'L2', style='invis')
dot.edge('L1', 'L3', style='invis')
dot.edge('L1', 'L4', style='invis')

# Save the source code and render the graph
dot.render('ecommerce_platform_architecture', format='png', cleanup=True)