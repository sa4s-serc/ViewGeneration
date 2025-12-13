from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Salesforce User CRUD System API Overview')

# Define nodes based on the components
dot.node('A', 'API Kit Router', shape='rectangle')
dot.node('B', 'Mule Flows', shape='rectangle')
dot.node('C', 'Salesforce Connector', shape='rectangle')
dot.node('D', 'Global Configuration', shape='rectangle')
dot.node('E', 'Client Applications', shape='rectangle')

# Define edges based on the interactions
dot.edge('E', 'A', label='REST API Calls', dir='forward')
dot.edge('A', 'B', label='Routes Requests', dir='forward')
dot.edge('B', 'C', label='Salesforce Operations', dir='forward')
dot.edge('B', 'D', label='Configuration Fetch', dir='forward')

# Add a subgraph for error handling and data transformation
with dot.subgraph(name='cluster_0') as c:
    c.node('F', 'Error Handling', shape='rectangle')
    c.node('G', 'Data Transformation', shape='rectangle')
    c.edges([('F', 'B'), ('G', 'B')])
    c.attr(label='Supporting Components', style='dashed')

# Add a legend
with dot.subgraph(name='cluster_1') as l:
    l.attr(label='Legend', style='dotted')
    l.node('L1', 'Rectangle: Component', shape='rectangle')
    l.node('L2', 'Arrow: Interaction', shape='plaintext')

# Render the diagram
dot.format = 'png'
dot.render('salesforce_user_crud_system_architecture')