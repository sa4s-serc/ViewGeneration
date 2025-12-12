from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='HTTP Proxy Service Architecture')

# Define nodes for each major component
dot.node('A', 'HttpProxyServer.java', shape='rect', style='filled', color='lightblue')
dot.node('B', 'ClientToProxyHandler.java', shape='rect', style='filled', color='lightblue')
dot.node('C', 'ProxyToServerInboundHandler.java', shape='rect', style='filled', color='lightblue')
dot.node('D', 'EntitysManager.java', shape='rect', style='filled', color='lightblue')
dot.node('E', 'GlobalExceptionHandler', shape='rect', style='filled', color='lightblue')
dot.node('F', 'TestClientApp.java', shape='rect', style='filled', color='lightgreen')
dot.node('G', 'TestServerMain.java', shape='rect', style='filled', color='lightgreen')
dot.node('H', 'entitys.json', shape='rect', style='filled', color='lightgrey')

# Define edges for communication flow
dot.edge('A', 'B', label='Initializes', arrowhead='vee')
dot.edge('B', 'C', label='Forwards Request', arrowhead='vee')
dot.edge('C', 'B', label='Sends Response', arrowhead='vee')
dot.edge('B', 'D', label='Fetches Proxy Entity', arrowhead='vee')
dot.edge('D', 'H', label='Loads/Reloads', arrowhead='vee')
dot.edge('A', 'E', label='Catches Exceptions', arrowhead='vee')
dot.edge('F', 'A', label='Sends Test Requests', arrowhead='vee')
dot.edge('G', 'A', label='Provides Test Endpoints', arrowhead='vee')

# Define legend
dot.node('Legend', 'Legend', shape='rect', style='filled', color='white')
dot.node('L1', 'Core Module', shape='rect', style='filled', color='lightblue')
dot.node('L2', 'Test Module', shape='rect', style='filled', color='lightgreen')
dot.node('L3', 'Configuration File', shape='rect', style='filled', color='lightgrey')

# Connect legend items
dot.edge('Legend', 'L1', arrowhead='none')
dot.edge('Legend', 'L2', arrowhead='none')
dot.edge('Legend', 'L3', arrowhead='none')

# Render the graph to a file
dot.render('http_proxy_service_architecture', format='png', cleanup=True)