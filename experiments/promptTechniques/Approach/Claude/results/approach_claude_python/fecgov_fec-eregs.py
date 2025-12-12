from graphviz import Digraph

dot = Digraph(comment='FEC ERegulations Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded')

# Add main components
dot.node('web', 'Web Interface\n(Django Templates)')
dot.node('api', 'API Layer')
dot.node('core', 'Core Application\n(Django)')
dot.node('db', 'PostgreSQL\n(MPTT Structure)')
dot.node('elastic', 'ElasticSearch\n(Search)')
dot.node('parser', 'Regulations Parser')
dot.node('cms', 'FEC CMS\nIntegration')
dot.node('cloud', 'Cloud Foundry\nInfrastructure')

# Add connections
dot.edge('web', 'api', 'HTTP/JSON')
dot.edge('api', 'core', 'Internal API')
dot.edge('core', 'db', 'Django ORM')
dot.edge('core', 'elastic', 'Search Queries')
dot.edge('parser', 'db', 'Regulation Updates')
dot.edge('web', 'cms', 'Content Integration')
dot.edge('cloud', 'web', 'Hosts')
dot.edge('cloud', 'db', 'Manages')
dot.edge('cloud', 'elastic', 'Manages')

# Print the source code
print(dot.source)

# Render the diagram
dot.render('fec_eregs_architecture', view=True, format='png')