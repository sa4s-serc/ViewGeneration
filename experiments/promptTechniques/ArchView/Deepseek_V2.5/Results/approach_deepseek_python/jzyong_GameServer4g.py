import graphviz

dot = graphviz.Digraph(comment='GameServer4g Architecture')
dot.attr(rankdir='TB', size='8,8')

with dot.subgraph(name='cluster_external') as c:
    c.attr(label='External', style='dashed', color='blue')
    c.node('client', 'Game Client', shape='ellipse', color='blue')

with dot.subgraph(name='cluster_gateway') as c:
    c.attr(label='Gateway Layer', style='rounded', color='red')
    c.node('gate', 'Gate Service', shape='box', color='red')
    c.node('user_manager', 'UserManager', shape='box', color='red')
    c.node('client_manager', 'ClientManager', shape='box', color='red')
    c.node('game_manager', 'GameManager', shape='box', color='red')

with dot.subgraph(name='cluster_hall') as c:
    c.attr(label='Hall Layer', style='rounded', color='green')
    c.node('hall', 'Hall Service', shape='box', color='green')
    c.node('hall_manager', 'HallManager', shape='box', color='green')

with dot.subgraph(name='cluster_world') as c:
    c.attr(label='World Layer', style='rounded', color='purple')
    c.node('world', 'World Service', shape='box', color='purple')
    c.node('world_manager', 'WorldManager', shape='box', color='purple')

with dot.subgraph(name='cluster_backend') as c:
    c.attr(label='Backend Services', style='rounded', color='orange')
    c.node('resource', 'Resource Service', shape='box', color='orange')
    c.node('api', 'API Service', shape='box', color='orange')
    c.node('manager', 'Manager Service', shape='box', color='orange')
    c.node('game_service', 'Game Service', shape='box', color='orange')

with dot.subgraph(name='cluster_infrastructure') as c:
    c.attr(label='Infrastructure', style='dashed', color='brown')
    c.node('zookeeper', 'ZooKeeper', shape='cylinder', color='brown')

dot.edge('client', 'gate', label='TCP/Custom Protocol', style='solid')
dot.edge('gate', 'hall', label='gRPC', style='dashed')
dot.edge('hall', 'world', label='gRPC', style='dashed')
dot.edge('gate', 'resource', label='gRPC', style='dashed')
dot.edge('gate', 'api', label='gRPC', style='dashed')
dot.edge('gate', 'manager', label='HTTP', style='dashed')
dot.edge('hall', 'game_service', label='gRPC', style='dashed')
dot.edge('world', 'resource', label='gRPC', style='dashed')

dot.edge('gate', 'zookeeper', label='Service Discovery', style='dotted')
dot.edge('hall', 'zookeeper', label='Service Discovery', style='dotted')
dot.edge('world', 'zookeeper', label='Service Discovery', style='dotted')

dot.edge('user_manager', 'client_manager', label='Internal', style='dotted')
dot.edge('client_manager', 'game_manager', label='Internal', style='dotted')
dot.edge('hall_manager', 'world_manager', label='Internal', style='dotted')

dot.render('gameserver4g_architecture', format='png', cleanup=True)