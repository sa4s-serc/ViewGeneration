import graphviz

dot = graphviz.Digraph(comment='Modern Data Architecture')
dot.attr(rankdir='TB', splines='ortho')

# Data Source
dot.node('kaggle_data', 'Kaggle Dataset\n(CSV Files)', shape='folder', style='filled', color='white')

# Data Ingestion Layer
with dot.subgraph(name='cluster_ingestion') as c:
    c.attr(label='Data Ingestion', style='filled', color='lightgrey')
    c.node('airbyte', 'Airbyte', shape='box', style='filled', color='lightblue')
    c.node('python_script', 'Python Script', shape='box', style='filled', color='lightblue')

# Data Warehousing Layer
with dot.subgraph(name='cluster_warehousing') as c:
    c.attr(label='Data Warehousing', style='filled', color='lightgrey')
    c.node('postgresql', 'PostgreSQL', shape='cylinder', style='filled', color='lightyellow')

# Data Transformation Layer
with dot.subgraph(name='cluster_transformation') as c:
    c.attr(label='Data Transformation', style='filled', color='lightgrey')
    c.node('dbt', 'DBT', shape='box', style='filled', color='lightgreen')

# Data Visualization Layer
with dot.subgraph(name='cluster_visualization') as c:
    c.attr(label='Data Visualization', style='filled', color='lightgrey')
    c.node('superset', 'Apache Superset', shape='box', style='filled', color='lightcoral')

# Orchestration
dot.node('docker', 'Docker &\nDocker Compose', shape='box', style='filled', color='lightpink')

# Data Flow Connections
dot.edge('kaggle_data', 'airbyte', label='extract', style='solid')
dot.edge('kaggle_data', 'python_script', label='extract\n(alternative)', style='dashed')
dot.edge('airbyte', 'postgresql', label='load', style='solid')
dot.edge('python_script', 'postgresql', label='load', style='dashed')
dot.edge('postgresql', 'dbt', label='transform', style='solid')
dot.edge('dbt', 'postgresql', label='write back', style='solid')
dot.edge('postgresql', 'superset', label='query', style='solid')

# Orchestration connections
dot.edge('docker', 'airbyte', style='dotted')
dot.edge('docker', 'postgresql', style='dotted')
dot.edge('docker', 'dbt', style='dotted')
dot.edge('docker', 'superset', style='dotted')

dot.render('modern_data_architecture', format='png', cleanup=True)