from graphviz import Digraph

dot = Digraph(comment='Decentraland Catalyst Content Server Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add main components
dot.node('api', 'API Endpoints\n(REST)')
dot.node('entity', 'Entity & Content\nManagement')
dot.node('sync', 'Synchronization\nComponent')
dot.node('storage', 'Storage\n(PostgreSQL + Files)')
dot.node('cache', 'Caching Layer\n(LRU)')
dot.node('validate', 'Validation &\nSecurity')
dot.node('graph', 'The Graph\nIntegration')
dot.node('third', 'Third-Party\nIntegration')

# Add connections
dot.edge('api', 'entity', 'requests')
dot.edge('entity', 'validate', 'validates')
dot.edge('validate', 'storage', 'persist')
dot.edge('entity', 'cache', 'cache data')
dot.edge('cache', 'storage', 'fetch/store')
dot.edge('entity', 'sync', 'sync state')
dot.edge('sync', 'storage', 'update')
dot.edge('entity', 'graph', 'query data')
dot.edge('entity', 'third', 'external content')

# Generate the diagram
dot.render('catalyst_architecture', view=True, format='png')