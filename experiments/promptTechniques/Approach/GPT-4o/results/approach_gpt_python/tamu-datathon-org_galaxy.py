from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Galaxy Repository Architecture', format='png')

# Define the nodes (components)
dot.node('GALAXY', 'Galaxy\nGateway')
dot.node('ROUTER', 'Router\nNginx')
dot.node('GATEKEEPER', 'Gatekeeper\nAuthentication')
dot.node('OBOS', 'Obos\nEvent Management')
dot.node('GIGABOWSER', 'Gigabowser\nStatic Website')

# Define edges (connectors) with unidirectional arrows
dot.edge('GALAXY', 'ROUTER', label='Handles Requests')
dot.edge('ROUTER', 'GATEKEEPER', label='Auth Requests')
dot.edge('ROUTER', 'OBOS', label='Event Requests')
dot.edge('ROUTER', 'GIGABOWSER', label='Static Content')

# Render the graph to a file
dot.render('galaxy_repository_architecture', view=True)