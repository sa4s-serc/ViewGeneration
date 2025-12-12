from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Veinmind-Tools Architecture', format='png')

# Define nodes for the main components
dot.node('A', 'Veinmind-Runner', shape='rectangle', style='filled', color='lightblue')
dot.node('B', 'Plugin A', shape='rectangle', style='filled', color='lightgrey')
dot.node('C', 'Plugin B', shape='rectangle', style='filled', color='lightgrey')
dot.node('D', 'Plugin C', shape='rectangle', style='filled', color='lightgrey')
dot.node('E', 'LibVeinmind', shape='rectangle', style='filled', color='lightcoral')

# Define nodes for the functionalities
dot.node('F', 'Malicious File Detection', shape='rectangle', style='filled', color='yellow')
dot.node('G', 'Weak Password Identification', shape='rectangle', style='filled', color='yellow')
dot.node('H', 'Unsafe Mount Point Detection', shape='rectangle', style='filled', color='yellow')
dot.node('I', 'CVE-specific Vulnerability Detection', shape='rectangle', style='filled', color='yellow')
dot.node('J', 'Intrusion Trace Detection', shape='rectangle', style='filled', color='yellow')
dot.node('K', 'Sensitive Information Detection', shape='rectangle', style='filled', color='yellow')

# Define edges for interactions
dot.edge('A', 'B', 'Manages')
dot.edge('A', 'C', 'Manages')
dot.edge('A', 'D', 'Manages')
dot.edge('B', 'E', 'Uses')
dot.edge('C', 'E', 'Uses')
dot.edge('D', 'E', 'Uses')

# Connect functionalities to LibVeinmind
dot.edge('E', 'F', 'Supports')
dot.edge('E', 'G', 'Supports')
dot.edge('E', 'H', 'Supports')
dot.edge('E', 'I', 'Supports')
dot.edge('E', 'J', 'Supports')
dot.edge('E', 'K', 'Supports')

# Render the graph
dot.render('veinmind_tools_architecture')