from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Hasses SSE Server Architecture')

# Add nodes for key components
dot.node('H', 'hasses.c (Main Server)')
dot.node('C', 'chat.c/h (SSE Logic)')
dot.node('D', 'cdata.c/h (Client Management)')
dot.node('I', 'cio.c/h (I/O Operations)')
dot.node('L', 'Logging')
dot.node('SSL', 'SSL/TLS (OpenSSL)')
dot.node('Conf', 'Configuration (hasses.conf)')

# Add nodes for external components
dot.node('WS', 'Web Server (Apache/Nginx)')
dot.node('Clients', 'Subscribed Clients')
dot.node('FIFO', 'FIFO File')
dot.node('TCP', 'TCP Socket')

# Add edges for interactions
dot.edge('WS', 'FIFO', label='Message Forwarding', style='dashed')
dot.edge('WS', 'TCP', label='Message Forwarding', style='dashed')
dot.edge('FIFO', 'H', label='Receive Messages')
dot.edge('TCP', 'H', label='Receive Messages')
dot.edge('H', 'C', label='SSE Handling')
dot.edge('H', 'D', label='Manage Clients')
dot.edge('H', 'I', label='Handle I/O')
dot.edge('H', 'L', label='Log Activities')
dot.edge('H', 'SSL', label='Secure Communication')
dot.edge('H', 'Conf', label='Read Settings')
dot.edge('C', 'Clients', label='Send Events')
dot.edge('D', 'Clients', label='Manage Connections')

# Add styles
dot.attr('node', shape='rectangle', style='filled', color='lightgrey')
dot.attr('edge', color='black', arrowsize='0.7')

# Render the graph to a file
dot.render('hasses_architecture', format='png', cleanup=True)