import graphviz

dot = graphviz.Digraph(comment='Decentraland Catalyst Content Server Architecture', engine='dot')

dot.attr(rankdir='TB', splines='ortho')

with dot.subgraph(name='cluster_external') as c:
    c.attr(label='External Services', style='dashed', color='blue')
    c.node('the_graph', 'The Graph', shape='cylinder')
    c.node('blockchain', 'Blockchain', shape='cylinder')
    c.node('third_party', 'Third-Party Services', shape='cylinder')
    c.node('content_storage', 'Content Storage', shape='cylinder')

with dot.subgraph(name='cluster_content_server') as c:
    c.attr(label='Content Server', style='filled', color='lightgrey')
    
    with c.subgraph(name='cluster_api') as api:
        api.attr(label='API Layer', style='rounded')
        api.node('server', 'Server (Express.js)', shape='ellipse')
        api.node('routes', 'Routes', shape='box')
        api.node('handlers', 'Handlers', shape='box')
        
    with c.subgraph(name='cluster_logic') as logic:
        logic.attr(label='Business Logic', style='rounded')
        logic.node('deployments', 'Deployments Logic', shape='box')
        logic.node('entity_parser', 'Entity Parser', shape='box')
        logic.node('synchronization', 'Synchronization', shape='box')
        logic.node('snapshots', 'Snapshots Logic', shape='box')
        logic.node('active_entities', 'Active Entity Management', shape='box')
        logic.node('collections', 'Collections API', shape='box')
        logic.node('profiles', 'Profiles Management', shape='box')
        logic.node('content_v2', 'Content V2 API', shape='box')
        
    with c.subgraph(name='cluster_validation') as val:
        val.attr(label='Validation & Security', style='rounded')
        val.node('validations', 'Validation Logic', shape='box')
        val.node('rate_limiting', 'Rate Limiting', shape='box')
        val.node('security', 'Security Checks', shape='box')
        
    with c.subgraph(name='cluster_data') as data:
        data.attr(label='Data Access', style='rounded')
        data.node('database', 'PostgreSQL', shape='cylinder')
        data.node('cache', 'LRU Cache', shape='box')
        data.node('bloom_filter', 'Bloom Filter', shape='box')
        data.node('migrations', 'Database Migrations', shape='box')
        
    with c.subgraph(name='cluster_utils') as utils:
        utils.attr(label='Utilities', style='rounded')
        utils.node('environment', 'Environment Config', shape='box')
        utils.node('metrics', 'Metrics Collection', shape='box')
        utils.node('garbage_collection', 'Garbage Collection', shape='box')
        utils.node('content_resizing', 'Content Resizing', shape='box')

dot.node('clients', 'Clients', shape='ellipse')

dot.edge('clients', 'server', label='REST API')
dot.edge('server', 'routes')
dot.edge('routes', 'handlers')
dot.edge('handlers', 'deployments')
dot.edge('handlers', 'active_entities')
dot.edge('handlers', 'collections')
dot.edge('handlers', 'profiles')
dot.edge('handlers', 'content_v2')

dot.edge('deployments', 'validations')
dot.edge('deployments', 'entity_parser')
dot.edge('deployments', 'database', label='persist')
dot.edge('deployments', 'content_storage', label='store content')

dot.edge('active_entities', 'cache')
dot.edge('active_entities', 'bloom_filter')
dot.edge('active_entities', 'database')

dot.edge('synchronization', 'snapshots')
dot.edge('synchronization', 'the_graph', label='fetch data')
dot.edge('synchronization', 'database', label='sync state')

dot.edge('profiles', 'the_graph', label='resolve ownership')
dot.edge('collections', 'third_party', label='query resolvers')
dot.edge('content_v2', 'database')

dot.edge('validations', 'security')
dot.edge('validations', 'rate_limiting')
dot.edge('security', 'blockchain', label='on-chain checks')

dot.edge('database', 'migrations')
dot.edge('cache', 'database', style='dashed')
dot.edge('bloom_filter', 'database', style='