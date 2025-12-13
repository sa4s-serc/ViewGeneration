from graphviz import Digraph

# Create a Digraph object
dot = Digraph(comment='Prometheus Monitoring Architecture', format='png')

# Define styles
styles = {
    'graph': {
        'label': 'Prometheus Monitoring Architecture',
        'fontsize': '16',
        'fontcolor': 'black',
        'bgcolor': 'white',
        'rankdir': 'LR'
    },
    'nodes': {
        'fontname': 'Helvetica',
        'shape': 'box',
        'fontcolor': 'black',
        'color': 'black',
        'style': 'filled',
        'fillcolor': '#eeeeee'
    },
    'edges': {
        'style': 'dashed',
        'color': 'black',
        'arrowhead': 'open'
    }
}

# Apply styles
dot.attr(**styles['graph'])
dot.node_attr.update(styles['nodes'])
dot.edge_attr.update(styles['edges'])

# Add nodes
dot.node('A', 'Sample Node.js Application\n(HTTP Server)')
dot.node('B', 'Prometheus\n(Time-Series DB)')
dot.node('C', 'Alertmanager')
dot.node('D', 'Grafana\n(Dashboard)')

# Add edges
dot.edge('A', 'B', label='Scrapes Metrics')
dot.edge('B', 'C', label='Sends Alerts')
dot.edge('B', 'D', label='Data Source')
dot.edge('C', 'D', label='Visualizes Alerts')

# Render and view the diagram
dot.render('prometheus_architecture', view=True)