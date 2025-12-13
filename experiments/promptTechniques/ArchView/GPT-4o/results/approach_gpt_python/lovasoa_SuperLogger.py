from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='System Monitoring with ELK Stack')

# Define nodes with distinct shapes and colors for different components
dot.node('A', 'Agent (Java)', shape='rectangle', style='filled', color='lightblue')
dot.node('L', 'Logstash', shape='rectangle', style='filled', color='lightgreen')
dot.node('E', 'Elasticsearch', shape='rectangle', style='filled', color='lightyellow')
dot.node('K', 'Kibana', shape='rectangle', style='filled', color='lightpink')

# Define edges with directional arrows to represent data flow
dot.edge('A', 'L', label='TCP', arrowhead='vee')
dot.edge('L', 'E', label='Processed Data', arrowhead='vee')
dot.edge('E', 'K', label='Stored Data', arrowhead='vee')

# Add a legend to describe the components and interactions
dot.node('Legend', 'Legend:\n\nA: Agent (Java)\nL: Logstash\nE: Elasticsearch\nK: Kibana\n\nData Flow:\nA -> L: TCP\nL -> E: Processed Data\nE -> K: Stored Data', shape='note', fontsize='10', color='grey')

# Position the legend
dot.edge('Legend', 'A', style='invis')

# Render the graph
dot.render('elk_stack_architecture', format='png', cleanup=True)