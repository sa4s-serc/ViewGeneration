import graphviz

# Create a new directed graph
dot = graphviz.Digraph(comment='HTTP Proxy Service Architecture')
dot.attr(rankdir='TB')

# Create clusters/subgraphs for logical grouping
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='HTTP Proxy Service')
    c.attr(style='rounded')
    c.attr(bgcolor='lightgrey')
    
    # Core proxy components
    c.node('proxy_server', 'HTTP Proxy Server\n(Netty)', shape='rectangle')
    c.node('client_handler', 'ClientToProxyHandler', shape='rectangle')
    c.node('server_handler', 'ProxyToServerHandler', shape='rectangle')
    c.node('entities_mgr', 'EntitiesManager', shape='rectangle')
    c.node('exception_handler', 'GlobalExceptionHandler', shape='rectangle')

with dot.subgraph(name='cluster_1') as c:
    c.attr(label='Filters')
    c.attr(style='rounded')
    c.attr(bgcolor='lightblue')
    c.node('req_filter', 'Request Filters\n(AttackRequestFilter)', shape='rectangle')
    c.node('resp_filter', 'Response Filters\n(DefaultProxyResponseFilter)', shape='rectangle')

with dot.subgraph(name='cluster_2') as c:
    c.attr(label='Configuration')
    c.attr(style='rounded')
    c.attr(bgcolor='lightgreen')
    c.node('config', 'entitys.json', shape='note')
    c.node('logging', 'Log4j2', shape='note')

# External components
dot.node('client', 'Client', shape='circle')
dot.node('backend', 'Backend Server', shape='circle')

# Add connections
dot.edge('client', 'proxy_server')
dot.edge('proxy_server', 'client_handler')
dot.edge('client_handler', 'req_filter')
dot.edge('req_filter', 'server_handler')
dot.edge('server_handler', 'backend')
dot.edge('backend', 'server_handler')
dot.edge('server_handler', 'resp_filter')
dot.edge('resp_filter', 'client_handler')
dot.edge('client_handler', 'client')

# Management connections
dot.edge('entities_mgr', 'config')
dot.edge('entities_mgr', 'proxy_server')
dot.edge('exception_handler', 'proxy_server')
dot.edge('proxy_server', 'logging')

# Save the diagram
dot.render('http_proxy_architecture', format='png', cleanup=True)