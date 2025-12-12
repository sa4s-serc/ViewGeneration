from graphviz import Digraph

dot = Digraph(comment='IRMA Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded')

# Core Components
dot.node('irmacall', 'irmacall\n(C Core Engine)')
dot.node('irmakit', 'irmakit\n(C# Framework)')
dot.node('fastcgi', 'FastCGI')
dot.node('mono', 'Mono Runtime')

# Storage and Cache
dot.node('memcached', 'Memcached')
dot.node('redis', 'Redis')
dot.node('kvstore', 'Key-Value Storage')

# External Services
dot.node('smtp', 'SMTP Server')
dot.node('openssl', 'OpenSSL')
dot.node('cares', 'c-ares\nDNS Resolution')

# Core Features
with dot.subgraph(name='cluster_features') as c:
    c.attr(label='Core Features')
    c.node('http_client', 'HTTP Client\n(curl)')
    c.node('logging', 'Logging System')
    c.node('crypto', 'Cryptography')
    c.node('fuse', 'Circuit Breaker')
    c.node('buffer', 'Buffer Pool')

# Framework Components
with dot.subgraph(name='cluster_framework') as c:
    c.attr(label='Framework Components')
    c.node('config', 'Configuration\nSystem')
    c.node('session', 'Session\nManagement')
    c.node('routing', 'Attribute-Driven\nRouting')
    c.node('templates', 'Template Engine')

# Define relationships
dot.edge('irmacall', 'fastcgi')
dot.edge('irmacall', 'mono')
dot.edge('mono', 'irmakit')
dot.edge('irmakit', 'config')
dot.edge('irmakit', 'session')
dot.edge('session', 'kvstore')
dot.edge('kvstore', 'memcached')
dot.edge('kvstore', 'redis')
dot.edge('irmacall', 'http_client')
dot.edge('irmacall', 'logging')
dot.edge('irmacall', 'crypto')
dot.edge('crypto', 'openssl')
dot.edge('irmacall', 'fuse')
dot.edge('irmacall', 'buffer')
dot.edge('irmacall', 'cares')
dot.edge('irmakit', 'routing')
dot.edge('irmakit', 'templates')
dot.edge('irmacall', 'smtp')

# Generate diagram
dot.render('irma_architecture', format='png', cleanup=True)