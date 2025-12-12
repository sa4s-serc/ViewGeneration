import graphviz

# Create a new directed graph
g = graphviz.Digraph('HeyBlue Architecture')
g.attr(rankdir='TB')

# Define node attributes
g.attr('node', shape='rectangle', style='rounded', fontname='Arial', fontsize='10')

# Add nodes for different layers
with g.subgraph(name='cluster_users') as c:
    c.attr(label='Users', style='rounded')
    c.node('civilians', 'Civilians')
    c.node('police', 'Police Officers')
    c.node('retailers', 'Retailers')

with g.subgraph(name='cluster_frontend') as c:
    c.attr(label='Frontend Layer')
    c.node('web_app', 'Web Application')
    c.node('mobile_app', 'Mobile App')
    c.node('bff', 'Backend for Frontend')

with g.subgraph(name='cluster_core') as c:
    c.attr(label='Core Services')
    c.node('auth', 'Authentication\n(AWS Cognito)')
    c.node('interaction', 'Interaction Service')
    c.node('points', 'Points Management')
    c.node('social', 'Social Graph')
    c.node('store', 'Storefront')

with g.subgraph(name='cluster_data') as c:
    c.attr(label='Data Layer')
    c.node('dynamodb', 'DynamoDB')
    c.node('s3', 'S3 Storage')
    c.node('analytics', 'Analytics\n(AWS Athena)')

# Add edges
g.edge('civilians', 'web_app')
g.edge('civilians', 'mobile_app')
g.edge('police', 'web_app')
g.edge('police', 'mobile_app')
g.edge('retailers', 'web_app')

g.edge('web_app', 'bff')
g.edge('mobile_app', 'bff')

g.edge('bff', 'auth')
g.edge('bff', 'interaction')
g.edge('bff', 'points')
g.edge('bff', 'store')

g.edge('interaction', 'social')
g.edge('points', 'dynamodb')
g.edge('store', 's3')
g.edge('social', 'dynamodb')

g.edge('dynamodb', 'analytics')
g.edge('s3', 'analytics')

# Set graph attributes
g.attr(label='HeyBlue System Architecture\nCloud-Native Social Platform', fontsize='16')

# Save the diagram
g.render('heyblue_architecture', format='png', cleanup=True)