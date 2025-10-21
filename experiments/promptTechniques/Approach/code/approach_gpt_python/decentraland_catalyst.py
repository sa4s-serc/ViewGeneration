from graphviz import Digraph

dot = Digraph(comment='Decentraland Catalyst Content Server Architecture')

# Components
dot.node('A', 'Entity and Content Retrieval', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('B', 'Content Deployment and Management', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('C', 'Active Entity Management', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('D', 'Synchronization', shape='rectangle', style='filled', fillcolor='lightgoldenrod')
dot.node('E', 'Third-Party Integration', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('F', 'Security and Validation', shape='rectangle', style='filled', fillcolor='lightpink')
dot.node('G', 'Collections API', shape='rectangle', style='filled', fillcolor='lightcyan')
dot.node('H', 'Garbage Collection', shape='rectangle', style='filled', fillcolor='lightyellow')
dot.node('I', 'API Endpoints', shape='rectangle', style='filled', fillcolor='lightsteelblue')
dot.node('J', 'Database Interaction', shape='rectangle', style='filled', fillcolor='lightseagreen')
dot.node('K', 'Caching', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('L', 'Rate Limiting', shape='rectangle', style='filled', fillcolor='lightgoldenrod')
dot.node('M', 'Metrics and Monitoring', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('N', 'Content Resizing', shape='rectangle', style='filled', fillcolor='lightpink')
dot.node('O', 'Migration', shape='rectangle', style='filled', fillcolor='lightcyan')

# Connectors
dot.edge('A', 'B', label='fetches')
dot.edge('B', 'C', label='deploys')
dot.edge('C', 'D', label='caches')
dot.edge('D', 'E', label='synchronizes')
dot.edge('E', 'F', label='integrates')
dot.edge('F', 'G', label='validates')
dot.edge('G', 'H', label='exposes')
dot.edge('H', 'I', label='removes')
dot.edge('I', 'J', label='exposes')
dot.edge('J', 'K', label='uses')
dot.edge('K', 'L', label='leverages')
dot.edge('L', 'M', label='limits')
dot.edge('M', 'N', label='collects')
dot.edge('N', 'O', label='provides')

# Render the diagram
dot.render('decentraland_catalyst_content_server_architecture', format='png', cleanup=True)