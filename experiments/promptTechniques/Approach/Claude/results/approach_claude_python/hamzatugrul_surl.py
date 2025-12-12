from graphviz import Digraph

dot = Digraph(comment='URL Shortener Service Architecture')
dot.attr(rankdir='TB')

# Styling
dot.attr('node', shape='rectangle', style='rounded')
dot.attr('edge', fontsize='10')

# Client Layer
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Client Layer', style='rounded')
    c.node('client', 'Client Applications')

# API Layer
with dot.subgraph(name='cluster_1') as c:
    c.attr(label='API Layer', style='rounded')
    c.node('nginx', 'Nginx Load Balancer')
    c.node('app1', 'App Instance 1')
    c.node('app2', 'App Instance 2')
    c.attr(rank='same')
    c.edge('app1', 'app2', dir='none', style='invisible')

# Service Layer
with dot.subgraph(name='cluster_2') as c:
    c.attr(label='Service Layer', style='rounded')
    c.node('shortener', 'URL Shortener Service')
    c.node('stats', 'Statistics Service')
    c.node('validator', 'URL Validator')

# Data Layer
with dot.subgraph(name='cluster_3') as c:
    c.attr(label='Data Layer', style='rounded')
    c.node('redis', 'Redis Cache', shape='cylinder')
    c.node('mongodb', 'MongoDB', shape='cylinder')

# Connections
dot.edge('client', 'nginx')
dot.edge('nginx', 'app1')
dot.edge('nginx', 'app2')
dot.edge('app1', 'shortener')
dot.edge('app2', 'shortener')
dot.edge('shortener', 'validator')
dot.edge('shortener', 'stats')
dot.edge('shortener', 'redis')
dot.edge('shortener', 'mongodb')
dot.edge('stats', 'mongodb')

dot.render('url_shortener_architecture', format='png', cleanup=True)