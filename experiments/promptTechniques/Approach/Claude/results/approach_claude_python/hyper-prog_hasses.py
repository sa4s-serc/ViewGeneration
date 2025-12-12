import graphviz

# Create a new directed graph
g = graphviz.Digraph('SSE Server Architecture')
g.attr(rankdir='TB')

# Define node attributes
g.attr('node', shape='rectangle', style='rounded', fontname='Arial')
g.attr('edge', fontname='Arial', fontsize='10')

# Create clusters/subgraphs
with g.subgraph(name='cluster_0') as c:
    c.attr(label='HASSES Core Components', style='rounded', color='gray')
    c.attr('node', style='filled', fillcolor='lightblue')
    
    # Core components
    c.node('epoll', 'epoll Event Loop\n(Non-blocking I/O)')
    c.node('chat', 'Chat Module\n(SSE Protocol Handler)')
    c.node('cdata', 'Client Data Manager\n(State & Subscriptions)')
    c.node('cio', 'I/O Handler\n(SSL/non-SSL)')

# External components
g.node('web_server', 'Web Server\n(Apache/Nginx)', shape='rectangle')
g.node('clients', 'SSE Clients', shape='rectangle')
g.node('fifo', 'FIFO/TCP Socket', shape='cylinder')

# Add edges with labels
g.edge('web_server', 'fifo', 'Forward messages')
g.edge('fifo', 'epoll', 'Message routing')
g.edge('clients', 'epoll', 'SSE connections')
g.edge('epoll', 'cio', 'I/O events')
g.edge('cio', 'chat', 'Protocol handling')
g.edge('chat', 'cdata', 'State updates')
g.edge('cdata', 'epoll', 'Subscription info')

# Save the diagram
g.render('sse_server_architecture', format='png', cleanup=True)