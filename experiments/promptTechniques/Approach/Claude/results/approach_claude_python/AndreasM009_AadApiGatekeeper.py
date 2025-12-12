import graphviz as gv

dot = gv.Digraph(name='AadApiGatekeeper_Architecture', 
                 comment='Architectural view of AAD API Gatekeeper',
                 format='png')

# Graph attributes
dot.attr(rankdir='TB')
dot.attr('node', shape='box', style='rounded')

# Add components
dot.node('client', 'Client Application')
dot.node('gatekeeper', 'AAD API Gatekeeper\n(Sidecar)')
dot.node('api', 'Backend API')
dot.node('aad', 'Azure AD')
dot.node('cache', 'Token Cache\n(In-Memory)')
dot.node('config', 'Configuration\n(Environment Variables)')

# Add subgraph for the main container environment
with dot.subgraph(name='cluster_container') as container:
    container.attr(label='Container Environment\n(Kubernetes/Service Fabric Mesh)')
    container.attr('node', shape='box', style='rounded')
    container.edge('gatekeeper', 'api', 'Forward Request')
    container.edge('gatekeeper', 'cache', 'Cache Token')

# Add external connections
dot.edge('client', 'gatekeeper', 'HTTP Request')
dot.edge('gatekeeper', 'aad', 'Validate Token/\nAcquire Token')
dot.edge('config', 'gatekeeper', 'Configure')

# Add authentication flow
dot.edge('client', 'aad', 'Authenticate', style='dashed')
dot.edge('aad', 'client', 'Issue Token', style='dashed')

if __name__ == "__main__":
    dot.render('aad_api_gatekeeper_architecture', view=True, cleanup=True)