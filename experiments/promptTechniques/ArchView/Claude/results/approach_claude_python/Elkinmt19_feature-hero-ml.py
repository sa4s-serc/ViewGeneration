import graphviz

# Create a new directed graph
dot = graphviz.Digraph(comment='Feature Hero ML Architecture')
dot.attr(rankdir='TB')
dot.attr(fontname='Arial')
dot.attr('node', shape='box', style='rounded', fontname='Arial', margin='0.3')
dot.attr('edge', fontname='Arial')

# Add clusters for logical grouping
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Data Layer', style='rounded', color='lightblue')
    c.node('minio', 'MinIO\nObject Storage')
    c.node('parquet', 'Parquet Files\nOffline Store')

with dot.subgraph(name='cluster_1') as c:
    c.attr(label='Feature Store Layer', style='rounded', color='lightgreen')
    c.node('feast', 'Feast\nFeature Store Framework')
    c.node('redis', 'Redis\nOnline Store')
    c.node('feature_server', 'Feature Server')

with dot.subgraph(name='cluster_2') as c:
    c.attr(label='Pipeline Layer', style='rounded', color='lightyellow')
    c.node('data_pipeline', 'Data Pipeline\nETL Process')
    c.node('precommit', 'Pre-commit Hooks\nCode Quality')

with dot.subgraph(name='cluster_3') as c:
    c.attr(label='Infrastructure Layer', style='rounded', color='lightgrey')
    c.node('docker', 'Docker & Docker Compose\nContainerization')

# Add edges
dot.edge('data_pipeline', 'parquet', 'Transform & Store')
dot.edge('parquet', 'feast', 'Offline Features')
dot.edge('feast', 'redis', 'Push Features')
dot.edge('redis', 'feature_server', 'Low-latency Serving')
dot.edge('feast', 'feature_server', 'Feature Registry')
dot.edge('minio', 'parquet', 'Store Files')
dot.edge('docker', 'feast', 'Containerize')
dot.edge('docker', 'redis', 'Containerize')
dot.edge('docker', 'minio', 'Containerize')
dot.edge('precommit', 'data_pipeline', 'Validate')

# Set title
dot.attr(label='Feature Hero ML Architecture\nFeature Store Implementation')
dot.attr(fontsize='16')

# Save the diagram
dot.render('feature_hero_architecture', format='png', cleanup=True)