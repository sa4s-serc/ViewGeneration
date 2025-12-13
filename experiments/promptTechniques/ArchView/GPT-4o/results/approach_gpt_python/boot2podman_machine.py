from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Podman Machine Architecture', format='png')

# Define the style attributes for the graph
dot.attr('node', shape='box', style='filled', color='lightgrey')
dot.attr('edge', style='solid')

# Core Functionality Components
dot.node('CLI', 'CLI Commands')
dot.node('Drivers', 'Drivers')
dot.node('Libmachine', 'Libmachine')
dot.node('Provisioners', 'Provisioners')
dot.node('Host', 'Host')
dot.node('Config', 'Configuration Files')
dot.node('Network', 'Network Components')

# Key Technologies
dot.node('Crypto', 'Cryptographic Libraries')
dot.node('Sys', 'System Call Interfaces')
dot.node('Spew', 'Debugging Tools')
dot.node('DiffLib', 'Diff Generation Tools')
dot.node('NaturalSort', 'Natural Sorting Tools')
dot.node('Testify', 'Testing Utilities')

# Relationships between components
dot.edge('CLI', 'Drivers', label='uses')
dot.edge('CLI', 'Libmachine', label='invokes')
dot.edge('Libmachine', 'Drivers', label='manages')
dot.edge('Libmachine', 'Provisioners', label='provisions')
dot.edge('Provisioners', 'Host', label='configures')
dot.edge('Host', 'Config', label='stores')
dot.edge('Host', 'Network', label='interfaces')

# Security and System Calls
dot.edge('Libmachine', 'Crypto', label='secures with')
dot.edge('Libmachine', 'Sys', label='executes')

# Other technologies
dot.edge('Libmachine', 'Spew', label='debugs with')
dot.edge('Libmachine', 'DiffLib', label='compares with')
dot.edge('Libmachine', 'NaturalSort', label='sorts with')
dot.edge('Libmachine', 'Testify', label='tests with')

# Render the graph to a file
dot.render('podman_machine_architecture')