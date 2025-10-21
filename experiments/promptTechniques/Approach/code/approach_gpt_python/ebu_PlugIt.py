from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='GitHub Repository Analysis Architecture')

# Define nodes with their types
dot.node('A', 'Repository', shape='cylinder', style='filled', fillcolor='lightgrey')
dot.node('B', 'Analysis Process', shape='box', style='filled', fillcolor='lightblue')
dot.node('C', 'Gemini API', shape='cylinder', style='filled', fillcolor='lightgrey')
dot.node('D', 'Error Handling', shape='box', style='filled', fillcolor='lightgreen')
dot.node('E', 'Retry Logic', shape='box', style='filled', fillcolor='lightgreen')
dot.node('F', 'Monitoring', shape='box', style='filled', fillcolor='lightgreen')

# Define edges with communication styles
dot.edge('A', 'B', 'invoke', dir='forward')
dot.edge('B', 'C', 'API Call', dir='forward')
dot.edge('C', 'D', '429 Error', dir='forward')
dot.edge('D', 'E', 'Trigger Retry', dir='forward')
dot.edge('B', 'F', 'Track Usage', dir='forward')

# Render the graph
dot.render('architecture_diagram', format='png', cleanup=True)