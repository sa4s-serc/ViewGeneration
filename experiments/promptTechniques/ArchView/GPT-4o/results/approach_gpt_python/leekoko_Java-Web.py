from graphviz import Digraph

def create_architecture_diagram():
    graph = Digraph('G', filename='architecture_diagram', format='png')

    # Define styles for nodes and edges
    node_style = {'shape': 'rect', 'style': 'filled', 'fillcolor': '#a3c1da'}
    edge_style = {'color': '#333333'}

    # Components
    graph.node('Java Web Application', **node_style)
    graph.node('jQuery Library', **node_style)
    graph.node('Dubbo Framework', **node_style)
    graph.node('Tomcat Server', **node_style)
    graph.node('Visitor Tracking', **node_style)
    graph.node('Backend', **node_style)
    graph.node('Frontend', **node_style)
    graph.node('Data Storage', **node_style)
    graph.node('Security', **node_style)
    graph.node('Dubbo Registry', **node_style)
    graph.node('Dubbo RPC', **node_style)
    graph.node('Tomcat Connectors', **node_style)

    # Relationships
    graph.edge('Java Web Application', 'Backend', **edge_style)
    graph.edge('Backend', 'Data Storage', **edge_style)
    graph.edge('Frontend', 'Backend', **edge_style)
    graph.edge('Java Web Application', 'Dubbo Framework', **edge_style)
    graph.edge('Dubbo Framework', 'Dubbo Registry', **edge_style)
    graph.edge('Dubbo Framework', 'Dubbo RPC', **edge_style)
    graph.edge('Tomcat Server', 'Tomcat Connectors', **edge_style)
    graph.edge('Visitor Tracking', 'Backend', **edge_style)
    graph.edge('Java Web Application', 'Security', **edge_style)
    graph.edge('Frontend', 'jQuery Library', **edge_style)

    # Render the diagram
    graph.render()

create_architecture_diagram()