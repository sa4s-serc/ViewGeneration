from graphviz import Digraph

dot = Digraph(comment='Pokemon Game Architecture')
dot.attr(rankdir='TB', splines='ortho')

# Define node styles
dot.attr('node', shape='rectangle', style='filled', fillcolor='lightblue')

# Add main components
dot.node('client', 'Client\n(Qt GUI)')
dot.node('server', 'Server\n(Multi-threaded)')
dot.node('db', 'SQLite Database')
dot.node('orm', 'ORM Layer')
dot.node('game_logic', 'Game Logic\n(Pokemon Classes)')
dot.node('gui', 'GUI Components')
dot.node('network', 'Network Layer\n(Sockets)')

# Add subcomponents
with dot.subgraph(name='cluster_client') as c:
    c.attr(label='Client Side')
    c.node('login', 'Login Widget')
    c.node('game_lobby', 'Game Lobby')
    c.node('battle', 'Battle System')
    c.node('user_bag', 'User Bag')

# Define relationships
dot.edge('client', 'network')
dot.edge('network', 'server')
dot.edge('server', 'orm')
dot.edge('orm', 'db')
dot.edge('server', 'game_logic')
dot.edge('client', 'gui')

# Connect client subcomponents
dot.edge('gui', 'login')
dot.edge('gui', 'game_lobby')
dot.edge('gui', 'battle')
dot.edge('gui', 'user_bag')

# Save the diagram
dot.render('pokemon_architecture', format='png', cleanup=True)