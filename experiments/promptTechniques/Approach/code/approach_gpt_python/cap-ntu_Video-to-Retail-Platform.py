from graphviz import Digraph

def create_architecture_diagram():
    dot = Digraph(comment='Hysia: Video-to-Retail Platform')

    # Nodes
    dot.node('V', 'Video Decoding', shape='rectangle', style='filled', fillcolor='lightblue')
    dot.node('D', 'Data Handling and Storage', shape='rectangle', style='filled', fillcolor='lightgreen')
    dot.node('M', 'Multimodal Data Processing', shape='rectangle', style='filled', fillcolor='lightcoral')
    dot.node('S', 'System Monitoring', shape='rectangle', style='filled', fillcolor='lightyellow')
    dot.node('A', 'API Layer', shape='rectangle', style='filled', fillcolor='lightgrey')
    dot.node('F', 'Frontend', shape='rectangle', style='filled', fillcolor='lightpink')
    dot.node('De', 'Deployment', shape='rectangle', style='filled', fillcolor='lightcyan')
    dot.node('ML', 'Machine Learning and Model Management', shape='rectangle', style='filled', fillcolor='lightgoldenrod')
    
    # Connections
    dot.edge('V', 'M', label='Processes', style='dashed')
    dot.edge('M', 'D', label='Stores Results', style='dotted')
    dot.edge('A', 'M', label='Communicates via REST/gRPC', style='bold')
    dot.edge('S', 'M', label='Monitors Performance', style='dotted')
    dot.edge('F', 'A', label='User Interaction', style='bold')
    dot.edge('De', 'ML', label='Model Deployment', style='dotted')
    
    # Styles
    dot.attr('node', shape='rectangle')
    dot.attr('graph', rankdir='LR')

    return dot

diagram = create_architecture_diagram()
diagram.render('hysia_architecture_diagram', format='png', cleanup=True)