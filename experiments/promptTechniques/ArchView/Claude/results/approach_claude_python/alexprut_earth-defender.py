from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Earth Defender Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Create client side cluster
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Client Side (Three.js)')
    c.node('game', 'Game\n(Core Game Loop)')
    c.node('client', 'GameClient\n(WebSocket Communication)') 
    c.node('dom', 'GameDOMHandler\n(UI Management)')
    c.node('elements', 'GameElements\n(Game Objects Factory)')
    c.node('texture', 'TextureLoader\n(Texture Cache)')
    c.node('objects', 'Game Objects\n(Earth, Ship, Meteorites)')

# Create server side cluster
with dot.subgraph(name='cluster_1') as c:
    c.attr(label='Server Side (Erlang/OTP)')
    c.node('ws_handler', 'websocket_handler\n(WebSocket Endpoint)')
    c.node('player', 'player\n(Player State)')
    c.node('room', 'room\n(Game Logic)')
    c.node('rooms_state', 'local_rooms_state\n(Room Management)')
    c.node('supervisor', 'earth_defender_sup\n(Process Supervisor)')
    c.node('monitor', 'monitor_mesh\n(Node Monitoring)')

# Add edges
dot.edge('game', 'client')
dot.edge('game', 'dom')
dot.edge('game', 'elements')
dot.edge('elements', 'texture')
dot.edge('elements', 'objects')

dot.edge('client', 'ws_handler')
dot.edge('ws_handler', 'player')
dot.edge('player', 'room')
dot.edge('room', 'rooms_state')
dot.edge('supervisor', 'ws_handler')
dot.edge('supervisor', 'player')
dot.edge('supervisor', 'room')
dot.edge('monitor', 'supervisor')

# Save the diagram
dot.render('earth_defender_architecture', format='png', cleanup=True)