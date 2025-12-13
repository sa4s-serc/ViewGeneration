from graphviz import Digraph

dot = Digraph(comment='OpenHub Architecture')

# Nodes for major components
dot.node('Crawler', 'Crawler: crawler.py', shape='rect', style='filled', fillcolor='lightblue')
dot.node('RabbitMQ', 'RabbitMQ', shape='rect', style='filled', fillcolor='orange')
dot.node('Worker', 'Worker: manager.py', shape='rect', style='filled', fillcolor='lightgreen')
dot.node('MongoDB', 'MongoDB', shape='cylinder', style='filled', fillcolor='lightgrey')

# Nodes for Analysis Modules
dot.node('Security', 'Security Analysis', shape='rect', style='filled', fillcolor='lightcoral')
dot.node('Testability', 'Testability Analysis', shape='rect', style='filled', fillcolor='lightcoral')
dot.node('Reusability', 'Reusability Analysis', shape='rect', style='filled', fillcolor='lightcoral')
dot.node('Usability', 'Usability Analysis', shape='rect', style='filled', fillcolor='lightcoral')

# Edges to represent control flow
dot.edge('Crawler', 'RabbitMQ', label='Publish Tasks', arrowhead='vee', style='dashed')
dot.edge('RabbitMQ', 'Worker', label='Consume Tasks', arrowhead='vee', style='dashed')
dot.edge('Worker', 'MongoDB', label='Store Results', arrowhead='vee', style='dashed')

# Edges for Analysis Modules
dot.edge('Worker', 'Security', label='Run Security Tests', arrowhead='vee', style='dotted')
dot.edge('Worker', 'Testability', label='Run Testability Tests', arrowhead='vee', style='dotted')
dot.edge('Worker', 'Reusability', label='Run Reusability Tests', arrowhead='vee', style='dotted')
dot.edge('Worker', 'Usability', label='Run Usability Tests', arrowhead='vee', style='dotted')

# Render the diagram
dot.render('openhub_architecture', format='png', cleanup=True)