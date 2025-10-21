from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Justice40 Tool Architecture')

# Add nodes for core components
dot.node('ETL', 'Data Pipeline (ETL)', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('Scoring', 'Scoring', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('MapTileGen', 'Map Tile Generation', shape='rectangle', style='filled', fillcolor='lightyellow')
dot.node('DataVal', 'Data Validation', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('ClientApp', 'Client-Side Application', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('CompTool', 'Comparison Tool', shape='rectangle', style='filled', fillcolor='lightpink')

# Add arrows for dynamic behavior and data flow
dot.edge('ETL', 'Scoring', label='Data Processed', arrowhead='open')
dot.edge('Scoring', 'MapTileGen', label='Scores Calculated', arrowhead='open')
dot.edge('MapTileGen', 'ClientApp', label='Map Tiles Generated', arrowhead='open')
dot.edge('ETL', 'DataVal', label='Data Integrity Checks', arrowhead='open')
dot.edge('ClientApp', 'CompTool', label='Interact with Comparison Tool', arrowhead='open')

# Add cluster for configuration and other key files
with dot.subgraph(name='cluster_config') as c:
    c.attr(style='filled', color='lightgrey')
    c.node('Docker', 'Docker Compose')
    c.node('Config', 'Configuration Files')
    c.node('Docs', 'Documentation')
    c.attr(label='Configuration & Documentation')

# Add edges for configuration influence
dot.edge('Docker', 'ETL', label='Microservice Setup', arrowhead='open')
dot.edge('Config', 'ETL', label='Pipeline Settings', arrowhead='open')
dot.edge('Config', 'Scoring', label='Scoring Config', arrowhead='open')

# Add legend
with dot.subgraph(name='cluster_legend') as l:
    l.attr(style='filled', color='white')
    l.node('Legend', 'Legend:\nBlue: ETL\nGreen: Scoring\nYellow: Map Tile\nRed: Validation\nGrey: Client\nPink: Comparison', shape='box', style='dashed')

# Render the graph to a file
dot.render('justice40_tool_architecture', format='png', cleanup=True)
print(dot.source)