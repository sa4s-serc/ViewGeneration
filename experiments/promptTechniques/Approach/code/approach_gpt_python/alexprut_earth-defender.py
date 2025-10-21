from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Earth Defender Architecture')

# Client-Side Components
dot.node('Game', 'Game')
dot.node('GameClient', 'GameClient')
dot.node('GameDOMHandler', 'GameDOMHandler')
dot.node('GameElements', 'GameElements')
dot.node('TextureLoader', 'TextureLoader')
dot.node('Light', 'Light')
dot.node('Earth', 'Earth')
dot.node('Sun', 'Sun')
dot.node('Moon', 'Moon')
dot.node('SpaceShip', 'SpaceShip')
dot.node('Bullet', 'Bullet')
dot.node('Meteorite', 'Meteorite')

# Server-Side Components
dot.node('slave_handler', 'slave_handler.erl')
dot.node('websocket_handler', 'websocket_handler.erl')
dot.node('player', 'player.erl')
dot.node('utils', 'utils.erl')
dot.node('local_rooms_state', 'local_rooms_state.erl')
dot.node('room', 'room.erl')
dot.node('earth_defender_sup', 'earth_defender_sup.erl')
dot.node('monitor_mesh', 'monitor_mesh.erl')
dot.node('earth_defender_app', 'earth_defender_app.erl')

# Communication and Interaction (Client-Server)
dot.edge('GameClient', 'websocket_handler', label='WebSocket Communication')
dot.edge('GameDOMHandler', 'Game', label='DOM Interaction')
dot.edge('Game', 'GameElements', label='Manage Game Objects')
dot.edge('Game', 'GameClient', label='Multiplayer Logic')
dot.edge('Game', 'TextureLoader', label='Load Textures')
dot.edge('Game', 'Light', label='Lighting Setup')
dot.edge('GameElements', 'Earth', label='Create Earth')
dot.edge('GameElements', 'Sun', label='Create Sun')
dot.edge('GameElements', 'Moon', label='Create Moon')
dot.edge('GameElements', 'SpaceShip', label='Create SpaceShip')
dot.edge('GameElements', 'Bullet', label='Create Bullet')
dot.edge('GameElements', 'Meteorite', label='Create Meteorite')

# Server-Side Logic
dot.edge('earth_defender_app', 'earth_defender_sup', label='Starts Supervisor')
dot.edge('earth_defender_sup', 'slave_handler', label='Manages Slave Servers')
dot.edge('earth_defender_sup', 'websocket_handler', label='Handles WebSockets')
dot.edge('earth_defender_sup', 'player', label='Manages Player States')
dot.edge('earth_defender_sup', 'local_rooms_state', label='Manages Game Rooms')
dot.edge('earth_defender_sup', 'room', label='Room Game Logic')
dot.edge('earth_defender_sup', 'monitor_mesh', label='Monitors Network')
dot.edge('earth_defender_sup', 'utils', label='Utility Functions')

# Output the diagram
dot.render('earth_defender_architecture', format='png', cleanup=True)