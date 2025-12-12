from graphviz import Digraph

dot = Digraph(comment='Apache APISIX Dashboard Front-End Architecture')

# Define styles
styles = {
    'graph': {
        'fontsize': '16',
        'label': 'Apache APISIX Dashboard Front-End Architecture',
        'labelloc': 't',
        'fontname': 'Helvetica'
    },
    'nodes': {
        'fontname': 'Helvetica',
        'shape': 'rectangle',
        'style': 'filled',
        'fillcolor': '#eeeeee',
        'fontsize': '10'
    },
    'edges': {
        'fontname': 'Helvetica',
        'fontsize': '10',
        'color': '#999999'
    }
}

# Apply styles
dot.graph_attr.update(styles['graph'])
dot.node_attr.update(styles['nodes'])
dot.edge_attr.update(styles['edges'])

# Define nodes
dot.node('A', 'React Components\n(UI Components, Forms)')
dot.node('B', 'Routing\n(TanStack Router)')
dot.node('C', 'State Management\n(MobX)')
dot.node('D', 'Data Fetching\n(TanStack Query)')
dot.node('E', 'API Abstraction\n(Axios)')
dot.node('F', 'Authentication')
dot.node('G', 'Plugin Management')
dot.node('H', 'Internationalization\n(react-i18next)')
dot.node('I', 'Real-time Updates')
dot.node('J', 'Error Handling\n(Mantine Notifications)')

# Define edges
dot.edge('A', 'B', 'Navigate')
dot.edge('B', 'C', 'Update State')
dot.edge('C', 'D', 'Fetch Data')
dot.edge('D', 'E', 'API Requests')
dot.edge('E', 'F', 'Auth Interceptors')
dot.edge('A', 'G', 'Manage Plugins')
dot.edge('A', 'H', 'i18n Support')
dot.edge('A', 'I', 'Realtime View')
dot.edge('A', 'J', 'Handle Errors')

# Render the diagram
dot.render('apache_apisix_dashboard_architecture', format='png', cleanup=True)