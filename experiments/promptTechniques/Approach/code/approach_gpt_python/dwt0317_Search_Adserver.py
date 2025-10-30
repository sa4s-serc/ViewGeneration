from graphviz import Digraph

def generate_architecture_diagram():
    dot = Digraph(comment='Search Ad Server Architecture')

    # Components
    dot.node('A', 'Servlets', shape='rectangle', style='filled', color='lightblue')
    dot.node('B', 'Ad Retrieval', shape='rectangle', style='filled', color='lightgreen')
    dot.node('C', 'Advertisement Entity', shape='rectangle', style='filled', color='lightcoral')
    dot.node('D', 'Query Rewriting', shape='rectangle', style='filled', color='lightyellow')
    dot.node('E', 'Elasticsearch Integration', shape='rectangle', style='filled', color='lightgrey')
    dot.node('F', 'Database Interaction', shape='rectangle', style='filled', color='lightpink')
    dot.node('G', 'Configuration', shape='rectangle', style='filled', color='lightcyan')
    dot.node('H', 'Initialization', shape='rectangle', style='filled', color='lightgoldenrod')
    dot.node('I', 'Frontend', shape='rectangle', style='filled', color='lightseagreen')

    # Connectors
    dot.edge('A', 'B', label='Handles HTTP Requests')
    dot.edge('B', 'C', label='Uses')
    dot.edge('B', 'D', label='Employs')
    dot.edge('B', 'E', label='Queries')
    dot.edge('B', 'F', label='Retrieves and Manages')
    dot.edge('G', 'H', label='Initializes')
    dot.edge('H', 'F', label='Connects to')
    dot.edge('I', 'A', label='User Interactions')

    # External Services (Thrift and Bing API)
    dot.node('J', 'Thrift Service', shape='ellipse', style='filled', color='lightsteelblue')
    dot.node('K', 'Bing API', shape='ellipse', style='filled', color='lightsteelblue')
    
    dot.edge('B', 'J', label='Delegates to')
    dot.edge('A', 'K', label='Interacts with')

    return dot

diagram = generate_architecture_diagram()
diagram.render('search_ad_server_architecture', format='png', cleanup=True)