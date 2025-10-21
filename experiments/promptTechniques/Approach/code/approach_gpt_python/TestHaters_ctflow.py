from graphviz import Digraph

# Initialize a directed graph
dot = Digraph(comment='CTFLOW Architecture', format='png')

# Define nodes for key components
dot.node('VSCode', 'VS Code Extension', shape='box', style='filled', color='lightblue')
dot.node('Webview', 'React-based Webview UI', shape='box', style='filled', color='lightgreen')
dot.node('Cypress', 'Cypress Testing Engine', shape='box', style='filled', color='lightcoral')
dot.node('Firebase', 'Firebase (Real-time Collaboration)', shape='box', style='filled', color='lightgrey')
dot.node('Graph', 'Visual Test Flow Graph', shape='ellipse', style='filled', color='lightyellow')

# Add edges to represent communication and interactions
dot.edge('VSCode', 'Webview', label='Hosts UI')
dot.edge('Webview', 'Cypress', label='Compile to Test Script')
dot.edge('Webview', 'Firebase', label='Real-time Sync (Potential)')
dot.edge('Webview', 'Graph', label='Visual Flow Representation')

# Visualize the diagram
dot.render('ctflow_architecture', view=True)