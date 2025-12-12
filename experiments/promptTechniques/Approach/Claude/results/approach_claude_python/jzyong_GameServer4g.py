import graphviz

# Create a new directed graph
dot = graphviz.Digraph(comment='GameServer4g Architecture')
dot.attr(rankdir='TB')

# Define subgraphs/clusters
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Game Server Architecture')
    c.attr(style='rounded')
    
    # Frontend/Client layer
    with c.subgraph(name='cluster_1') as front:
        front.attr(label='Frontend Layer', style='rounded')
        front.node('client', 'Game Client', shape='rectangle')
        front.node('gate', 'Gate Service\n(Connection Management)\nUserManager\nGameManager', shape='rectangle')

    # Game Logic layer
    with c.subgraph(name='cluster_2') as logic:
        logic.attr(label='Game Logic Layer', style='rounded')
        logic.node('hall', 'Hall Service\n(Game Logic)\nHallManager\nMatchmaking', shape='rectangle')
        logic.node('world', 'World Service\n(Game World)\nWorldManager\nEntities', shape='rectangle')

    # Support Services layer
    with c.subgraph(name='cluster_3') as support:
        support.attr(label='Support Layer', style='rounded')
        support.node('res', 'Resource Service', shape='rectangle')
        support.node('api', 'API Service\n(Login/Charge)', shape='rectangle')
        support.node('manager', 'Manager Service\n(Admin HTTP)', shape='rectangle')
        support.node('zk', 'ZooKeeper\n(Service Discovery)', shape='rectangle')

# Add connections with labels
dot.edge('client', 'gate', 'TCP Protocol')
dot.edge('gate', 'hall', 'gRPC')
dot.edge('hall', 'world', 'gRPC\n(Player Actions)')
dot.edge('gate', 'zk', 'Service Registration')
dot.edge('hall', 'zk', 'Service Discovery')
dot.edge('world', 'zk', 'Service Registration')
dot.edge('client', 'api', 'HTTP')
dot.edge('api', 'hall', 'Internal API')
dot.edge('manager', 'hall', 'HTTP Admin')
dot.edge('manager', 'world', 'HTTP Admin')
dot.edge('hall', 'res', 'Support Services')
dot.edge('world', 'res', 'Support Services')

# Set graph styling
dot.attr(fontsize='16')
dot.attr('node', fontsize='12')
dot.attr('edge', fontsize='10')

# Save the diagram
dot.render('gameserver4g_architecture', format='png', cleanup=True)