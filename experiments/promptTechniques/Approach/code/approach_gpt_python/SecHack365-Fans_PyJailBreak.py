from graphviz import Digraph

dot = Digraph(comment='PyJailBreak Frontend Architecture')

# Define nodes for components
dot.node('A', 'UI for Scan Configuration', shape='rectangle', style='filled', color='lightblue')
dot.node('B', 'Payload Management', shape='rectangle', style='filled', color='lightgrey')
dot.node('C', 'Vulnerability Scan Execution', shape='rectangle', style='filled', color='lightblue')
dot.node('D', 'Emulation Mode', shape='rectangle', style='filled', color='lightgrey')
dot.node('E', 'Configuration', shape='rectangle', style='filled', color='lightblue')
dot.node('F', 'API Documentation', shape='rectangle', style='filled', color='lightgrey')

# Define edges for communication
dot.edge('A', 'C', label='Configure and Launch Scans', style='dashed')
dot.edge('B', 'C', label='Manage Payloads', style='dashed')
dot.edge('C', 'E', label='Execute Scans', style='dashed')
dot.edge('D', 'C', label='Simulate Attacks', style='dashed')
dot.edge('E', 'F', label='Access API Documentation', style='dashed')

# Legend
dot.node('L1', 'Frontend Component', shape='rectangle', style='filled', color='lightblue')
dot.node('L2', 'State Management Component', shape='rectangle', style='filled', color='lightgrey')

# Display the graph
print(dot.source)
dot.render('pyjailbreak_frontend_architecture', view=True)