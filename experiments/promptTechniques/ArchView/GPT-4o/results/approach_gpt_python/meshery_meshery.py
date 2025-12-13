from graphviz import Digraph

def generate_meshery_architecture_diagram():
    dot = Digraph('Meshery Architecture', node_attr={'shape': 'box', 'style': 'filled', 'fillcolor': 'lightgrey'})

    # Core Components
    dot.node('Meshery Server', 'Meshery Server', fillcolor='lightblue')
    dot.node('Meshery UI', 'Meshery UI', fillcolor='lightblue')
    dot.node('mesheryctl', 'mesheryctl (CLI)', fillcolor='lightblue')
    dot.node('Meshery Operator', 'Meshery Operator', fillcolor='lightblue')
    dot.node('MeshKit', 'MeshKit', fillcolor='lightblue')
    dot.node('Event Broker', 'Event Broker (NATS)', fillcolor='lightblue')
    
    # Architecture Styles
    dot.node('Adapters', 'Adapters', fillcolor='lightgreen')
    dot.node('GraphQL API', 'GraphQL API', fillcolor='lightgreen')
    dot.node('Providers', 'Providers', fillcolor='lightgreen')
    dot.node('MeshSync', 'MeshSync', fillcolor='lightgreen')
    
    # Communication
    dot.edge('Meshery Server', 'Adapters', label='gRPC')
    dot.edge('Meshery Server', 'Meshery UI', label='GraphQL')
    dot.edge('Meshery Server', 'mesheryctl', label='CLI Commands')
    dot.edge('Meshery Server', 'Event Broker', label='Event Driven')
    dot.edge('Meshery Operator', 'MeshSync', label='Kubernetes Sync')
    
    # Data Management
    dot.node('Data Models', 'Data Models', fillcolor='lightcoral')
    dot.node('Components', 'Components', fillcolor='lightcoral')
    dot.node('Designs', 'Designs', fillcolor='lightcoral')
    
    # Relationships
    dot.edge('Meshery Server', 'Data Models', label='Model Driven')
    dot.edge('Data Models', 'Components', label='Configurable')
    dot.edge('Components', 'Designs', label='Reusable')
    
    # Non-functional Requirements
    dot.node('Scalability', 'Scalability', fillcolor='lightyellow')
    dot.node('Extensibility', 'Extensibility', fillcolor='lightyellow')
    dot.node('Performance', 'Performance', fillcolor='lightyellow')
    
    # Highlight Non-functional Aspects
    dot.edge('Meshery Server', 'Scalability')
    dot.edge('Meshery Server', 'Extensibility')
    dot.edge('Meshery UI', 'Performance')

    return dot

# Generate and render the diagram
diagram = generate_meshery_architecture_diagram()
diagram.format = 'png'
diagram.render('meshery_architecture_diagram', view=True)