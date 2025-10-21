from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Minism Hotel Architecture', format='png')

# Define the nodes with specific styles
dot.node('Master Server', 'Master Server\n(hotel-master)', shape='rect', style='filled', color='lightblue')
dot.node('REST API', 'REST API', shape='rect', style='filled', color='lightgrey')
dot.node('RPC Server', 'RPC gRPC Server', shape='rect', style='filled', color='lightgrey')
dot.node('Session Management', 'Session Management\n(SessionStore)', shape='rect', style='filled', color='lightgrey')
dot.node('Database', 'Database\n(SQLite)', shape='rect', style='filled', color='lightgrey')
dot.node('Reaper', 'Reaper', shape='rect', style='filled', color='lightgrey')

dot.node('Spawner', 'Spawner\n(hotel-spawner)', shape='rect', style='filled', color='lightcoral')
dot.node('Spawner RPC', 'RPC gRPC Server', shape='rect', style='filled', color='lightgrey')
dot.node('Game Server Management', 'Game Server Management', shape='rect', style='filled', color='lightgrey')

dot.node('Shared Libraries', 'Shared Libraries', shape='rect', style='filled', color='lightgreen')
dot.node('Configuration', 'Configuration Loading', shape='rect', style='filled', color='lightgrey')
dot.node('Logging', 'Logging', shape='rect', style='filled', color='lightgrey')
dot.node('Crypto', 'Crypto', shape='rect', style='filled', color='lightgrey')

# Define the edges with specific styles
dot.edge('Master Server', 'REST API', label='HTTP', style='dashed')
dot.edge('Master Server', 'RPC Server', label='gRPC', style='dashed')
dot.edge('Master Server', 'Session Management', label='Singleton', style='dashed')
dot.edge('Master Server', 'Database', label='Data Access', style='dashed')
dot.edge('Master Server', 'Reaper', label='Background Process', style='dashed')

dot.edge('Spawner', 'Spawner RPC', label='gRPC', style='dashed')
dot.edge('Spawner', 'Game Server Management', label='Exec/Monitor', style='dashed')

dot.edge('Shared Libraries', 'Configuration', style='dashed')
dot.edge('Shared Libraries', 'Logging', style='dashed')
dot.edge('Shared Libraries', 'Crypto', style='dashed')

dot.edge('Spawner', 'Master Server', label='Registration/Status', dir='both', style='solid')
dot.edge('Spawner RPC', 'Master Server', label='Spawn Requests', dir='both', style='solid')

# Render the diagram
dot.render('minism_hotel_architecture', view=True)