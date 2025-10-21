from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='IRMA Efficient Web Service Framework')

# Define node shapes and styles
dot.node('A', 'irmacall Core Engine', shape='box', style='filled', color='lightblue')
dot.node('B', 'irmakit Framework', shape='box', style='filled', color='lightgreen')

# Define core functionalities of irmacall
dot.node('C1', 'Request Handling', shape='ellipse')
dot.node('C2', 'HTTP Client (Fetcher)', shape='ellipse')
dot.node('C3', 'Key-Value Storage Abstraction', shape='ellipse')
dot.node('C4', 'Logging', shape='ellipse')
dot.node('C5', 'SMTP Support', shape='ellipse')
dot.node('C6', 'Cryptography', shape='ellipse')
dot.node('C7', 'Fuse (Circuit Breaker)', shape='ellipse')
dot.node('C8', 'Buffer Management', shape='ellipse')
dot.node('C9', 'Asynchronous DNS Resolution', shape='ellipse')

# Define core functionalities of irmakit
dot.node('D1', 'Configuration System', shape='ellipse')
dot.node('D2', 'Session Management', shape='ellipse')
dot.node('D3', 'Request and Response Handling', shape='ellipse')
dot.node('D4', 'Attribute-Driven Routing', shape='ellipse')
dot.node('D5', 'Template Engine Integration', shape='ellipse')
dot.node('D6', 'Utilities', shape='ellipse')
dot.node('D7', 'Code Generation', shape='ellipse')

# Define connections between components
dot.edges([('A', 'C1'), ('A', 'C2'), ('A', 'C3'), ('A', 'C4'), ('A', 'C5'), ('A', 'C6'), ('A', 'C7'), ('A', 'C8'), ('A', 'C9')])
dot.edges([('B', 'D1'), ('B', 'D2'), ('B', 'D3'), ('B', 'D4'), ('B', 'D5'), ('B', 'D6'), ('B', 'D7')])

# Define communication between irmacall and irmakit
dot.edge('A', 'B', label='Schedules Applications')

# Render the graph to a file
dot.render('irma_architecture_diagram', format='png', cleanup=True)