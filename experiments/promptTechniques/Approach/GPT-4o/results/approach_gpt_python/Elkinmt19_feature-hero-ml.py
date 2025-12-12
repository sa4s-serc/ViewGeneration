from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Feature Hero ML: Feature Store Repository Analysis')

# Define styles for different components
styles = {
    'node': {
        'fontname': 'Helvetica',
        'shape': 'rectangle',
        'style': 'filled',
        'fillcolor': '#D3D3D3',
        'color': 'black'
    },
    'edge': {
        'color': 'black',
        'arrowhead': 'open',
    }
}

# Apply styles to the graph
dot.attr('node', **styles['node'])
dot.attr('edge', **styles['edge'])

# Define nodes for key components
dot.node('FS', 'Feature Store (Feast)')
dot.node('R', 'Redis (Online Store)')
dot.node('P', 'Parquet (Offline Store)')
dot.node('D', 'Docker & Docker Compose')
dot.node('C', 'Configuration Management')
dot.node('ETL', 'Data Pipeline (ETL)')

# Define edges for data flow and interactions
dot.edge('ETL', 'FS', label='Ingest Features')
dot.edge('FS', 'R', label='Low-latency Access')
dot.edge('FS', 'P', label='Batch Processing')
dot.edge('D', 'FS', label='Containerized Deployment')
dot.edge('C', 'FS', label='Centralized Config')

# Render the graph
dot.render('feature_hero_ml_architecture', format='png', cleanup=True)