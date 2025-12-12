import graphviz as gv

# Create a new directed graph
dot = gv.Digraph(comment='Modern Data Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded,filled', fontname='Arial')
dot.attr('edge', fontname='Arial')

# Add components with colors
dot.node('airbyte', 'Airbyte\nData Extraction', fillcolor='lightblue')
dot.node('postgres', 'PostgreSQL\nData Warehouse', fillcolor='lightgreen')
dot.node('dbt', 'DBT\nData Transformation', fillcolor='lightyellow')
dot.node('superset', 'Apache Superset\nVisualization', fillcolor='lightpink')
dot.node('python', 'Python Script\nAlternative Loader', fillcolor='lightgrey')

# Add connections
dot.edge('airbyte', 'postgres', 'Extract & Load')
dot.edge('python', 'postgres', 'Direct Load')
dot.edge('postgres', 'dbt', 'Raw Data')
dot.edge('dbt', 'postgres', 'Transformed Data')
dot.edge('postgres', 'superset', 'Analytics Queries')

# Add subgraph for data flow
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Data Flow Pipeline')
    c.attr('node', style='filled')
    c.edges([('airbyte', 'postgres'), ('postgres', 'dbt'), ('dbt', 'postgres')])

# Save the diagram
dot.render('modern_data_architecture', format='png', cleanup=True)