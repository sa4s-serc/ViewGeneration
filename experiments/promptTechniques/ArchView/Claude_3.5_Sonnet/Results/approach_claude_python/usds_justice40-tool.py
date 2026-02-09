from graphviz import Digraph

dot = Digraph(comment='Justice40 Tool Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded')

# Add main components
dot.node('data_pipeline', 'Data Pipeline (ETL)')
dot.node('scoring', 'Scoring System')
dot.node('map_tiles', 'Map Tile Generation')
dot.node('validation', 'Data Validation')
dot.node('client', 'Client-Side Application')
dot.node('comparison', 'Comparison Tool')
dot.node('s3', 'S3 Data Lake')

# Add subcomponents
with dot.subgraph(name='cluster_etl') as etl:
    etl.attr(label='ETL Components')
    etl.node('runner', 'runner.py')
    etl.node('base', 'base.py')
    etl.node('datasource', 'datasource.py')

with dot.subgraph(name='cluster_client') as client_components:
    client_components.attr(label='Client Components')
    client_components.node('react', 'React Frontend')
    client_components.node('maplibre', 'MapLibre GL')
    client_components.node('i18n', 'Internationalization')

# Add edges
dot.edge('datasource', 'base')
dot.edge('base', 'runner')
dot.edge('runner', 'data_pipeline')
dot.edge('data_pipeline', 's3')
dot.edge('s3', 'scoring')
dot.edge('scoring', 'map_tiles')
dot.edge('s3', 'validation')
dot.edge('map_tiles', 'client')
dot.edge('react', 'maplibre')
dot.edge('i18n', 'react')
dot.edge('s3', 'comparison')

# Print the dot source
print(dot.source)

# Render the diagram
dot.render('justice40_architecture', format='png', cleanup=True)