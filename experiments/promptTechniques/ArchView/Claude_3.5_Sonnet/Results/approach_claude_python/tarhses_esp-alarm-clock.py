from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='ESP32 Alarm Clock Architecture')

# Set graph attributes
dot.attr(rankdir='TB', splines='ortho')
dot.attr('node', shape='rectangle', style='rounded')

# Create clusters for grouping related components
with dot.subgraph(name='cluster_core') as core:
    core.attr(label='Core Components', style='rounded', color='blue')
    core.node('main', 'Main Application\n(main.c)\nSystem Initialization\nTask Coordination', shape='component')
    core.node('alarm', 'Alarm Module\n(alarm.c)\nAlarm Logic\nEvent Handling', shape='component') 
    core.node('network', 'Network Module\n(network.c)\nWiFi & SNTP', shape='component')
    core.node('display', 'Display Module\n(display.c)\nE-Paper Control', shape='component')

with dot.subgraph(name='cluster_io') as io:
    io.attr(label='I/O Components', style='rounded', color='green')
    io.node('sound', 'Sound Module\n(sound.c)\nAudio Playback', shape='component')
    io.node('pot', 'Potentiometer Module\n(pot.c)\nTime Setting', shape='component')
    io.node('storage', 'Storage Module\n(storage.c)\nSD & NVS', shape='component')

# External interfaces
dot.attr('node', shape='cylinder', style='filled', fillcolor='lightgray')
dot.node('sd', 'SD Card\nConfig & Audio')
dot.node('nvs', 'NVS Storage\nCalibration')

dot.attr('node', shape='diamond', style='filled', fillcolor='lightblue')
dot.node('wifi', 'WiFi\nConnection')
dot.node('ntp', 'NTP Server\nTime Sync')

dot.attr('node', shape='box3d', style='filled', fillcolor='lightgreen') 
dot.node('epaper', 'E-Paper Display')
dot.node('speaker', 'Speaker')
dot.node('pots', 'Potentiometers')

# Define edges with labels
dot.edge('main', 'alarm', 'initialize')
dot.edge('main', 'network', 'initialize')
dot.edge('main', 'display', 'initialize')
dot.edge('main', 'sound', 'initialize')
dot.edge('main', 'pot', 'initialize')
dot.edge('main', 'storage', 'initialize')

dot.edge('network', 'wifi', 'connect')
dot.edge('network', 'ntp', 'sync')
dot.edge('storage', 'sd', 'read/write')
dot.edge('storage', 'nvs', 'persist')
dot.edge('display', 'epaper', 'render')
dot.edge('sound', 'speaker', 'play')
dot.edge('pot', 'pots', 'read')

dot.edge('alarm', 'sound', 'trigger alarm')
dot.edge('alarm', 'display', 'update time')
dot.edge('pot', 'alarm', 'set alarm time')
dot.edge('network', 'alarm', 'sync time')

# Save the diagram
dot.render('esp32_alarm_architecture', format='png', cleanup=True)