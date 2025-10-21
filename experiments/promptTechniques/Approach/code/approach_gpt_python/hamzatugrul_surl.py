from graphviz import Digraph

# Create a Digraph object
dot = Digraph(comment='URL Shortener Service Architecture')

# Define clusters for layers
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Client Layer')
    c.node('Client', 'Client')
    
with dot.subgraph(name='cluster_1') as c:
    c.attr(label='Load Balancer Layer')
    c.node('Nginx', 'Nginx')
    
with dot.subgraph(name='cluster_2') as c:
    c.attr(label='Application Layer')
    c.node('API', 'REST API')
    c.node('Controller', 'ShortURLController')
    c.node('Service', 'UrlShortenerService')
    c.node('KeyGen', 'Murmur3With32BitsHashKeyGenerator')
    c.node('Validator', 'SUrlValidator')
    
with dot.subgraph(name='cluster_3') as c:
    c.attr(label='Data Layer')
    c.node('MongoDB', 'MongoDB', shape='cylinder')
    c.node('Redis', 'Redis', shape='cylinder')

# Define edges
dot.edge('Client', 'Nginx', label='HTTP Request')
dot.edge('Nginx', 'API', label='Load Balanced Request')
dot.edge('API', 'Controller', label='Invoke')
dot.edge('Controller', 'Service', label='Call')
dot.edge('Service', 'MongoDB', label='Persist Data')
dot.edge('Service', 'Redis', label='Cache Data')
dot.edge('Service', 'KeyGen', label='Generate Key')
dot.edge('Service', 'Validator', label='Validate URL')
dot.edge('MongoDB', 'Service', label='Retrieve Data', dir='back')
dot.edge('Redis', 'Service', label='Retrieve Cache', dir='back')

# Define styles
dot.attr('node', shape='rectangle')

# Render or view the diagram
dot.render('url_shortener_service_architecture', format='png', cleanup=True)  # This will save the diagram as a PNG file.