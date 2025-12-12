from graphviz import Digraph

dot = Digraph(comment='Minism Hotel Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add main components
dot.node('master', 'Hotel Master Server\n(hotel-master)')
dot.node('spawner', 'Hotel Spawner\n(hotel-spawner)')
dot.node('db', 'SQLite Database')
dot.node('rest', 'REST API')
dot.node('rpc', 'gRPC Server')
dot.node('session', 'Session Management')
dot.node('reaper', 'Reaper Process')
dot.node('game', 'Game Servers')
dot.node('config', 'Configuration')
dot.node('proto', 'Protobuf\nCommunication')

# Add edges
dot.edge('master', 'rest', 'HTTP')
dot.edge('master', 'rpc', 'gRPC')
dot.edge('master', 'db', 'Data Access')
dot.edge('master', 'session', 'Manages')
dot.edge('master', 'reaper', 'Runs')
dot.edge('spawner', 'rpc', 'gRPC')
dot.edge('spawner', 'game', 'Executes')
dot.edge('game', 'master', 'Registers')
dot.edge('config', 'master', 'Configures')
dot.edge('config', 'spawner', 'Configures')
dot.edge('proto', 'master', 'Defines')
dot.edge('proto', 'spawner', 'Defines')

# Set graph attributes
dot.attr(label='Minism Hotel Architecture\nMaster-Spawner Game Server Management System')
dot.attr(fontsize='16')

# Render the graph
dot.render('minism_hotel_architecture', format='png', cleanup=True)