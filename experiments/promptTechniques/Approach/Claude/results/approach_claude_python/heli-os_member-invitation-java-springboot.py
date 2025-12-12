from graphviz import Digraph

dot = Digraph(comment='Member Invitation System Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightgrey')

# Create main layers
dot.node('api_layer', 'API Layer\n(REST Controllers)')
dot.node('domain_layer', 'Domain Layer\n(Use Cases & Services)')
dot.node('infra_layer', 'Infrastructure Layer')

# Create infrastructure components
with dot.subgraph(name='cluster_infra') as infra:
    infra.attr(label='Infrastructure Components')
    infra.node('redis', 'Redis\n(Invitation Storage)', fillcolor='lightblue')
    infra.node('db', 'Database\n(Member Storage)', fillcolor='lightblue')

# Create domain components
with dot.subgraph(name='cluster_domain') as domain:
    domain.attr(label='Domain Components')
    domain.node('invitation_service', 'Invitation Service')
    domain.node('member_service', 'Member Service')

# Create API endpoints
with dot.subgraph(name='cluster_api') as api:
    api.attr(label='REST Endpoints')
    api.node('invitation_api', '/api/v1/invitation/*')
    api.node('workspace_api', '/api/v1/workspace/*')
    api.node('member_api', '/api/v1/member/*')

# Define relationships
dot.edge('api_layer', 'domain_layer', 'Uses')
dot.edge('domain_layer', 'infra_layer', 'Uses')
dot.edge('invitation_api', 'invitation_service', 'Calls')
dot.edge('workspace_api', 'invitation_service', 'Calls')
dot.edge('member_api', 'member_service', 'Calls')
dot.edge('invitation_service', 'redis', 'Stores Invitations')
dot.edge('member_service', 'db', 'Stores Members')

# Save the diagram
dot.render('member_invitation_architecture', format='png', cleanup=True)