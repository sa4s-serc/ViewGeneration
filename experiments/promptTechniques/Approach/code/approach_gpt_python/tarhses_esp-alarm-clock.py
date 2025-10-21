from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='ESP32 Alarm Clock Architecture', format='png')

# Set graph attributes
dot.attr(rankdir='TB', size='10,8')

# Define colors for different module types
module_color = 'lightblue'
component_color = 'lightgrey'

# Add nodes for each main module
dot.node('main.c', 'Main Application', shape='box', style='filled', fillcolor=module_color)
dot.node('alarm.c', 'Alarm Management', shape='box', style='filled', fillcolor=module_color)
dot.node('network.c', 'Networking', shape='box', style='filled', fillcolor=module_color)
dot.node('display.c', 'Display Control', shape='box', style='filled', fillcolor=module_color)
dot.node('sound.c', 'Sound Management', shape='box', style='filled', fillcolor=module_color)
dot.node('pot.c', 'Potentiometer Handling', shape='box', style='filled', fillcolor=module_color)
dot.node('storage.c', 'Storage Management', shape='box', style='filled', fillcolor=module_color)

# Add components within the modules
dot.node('sntp', 'SNTP Synchronization', shape='ellipse', style='filled', fillcolor=component_color)
dot.node('e-paper', 'E-Paper Display', shape='ellipse', style='filled', fillcolor=component_color)
dot.node('wifi', 'WiFi Connectivity', shape='ellipse', style='filled', fillcolor=component_color)
dot.node('nvs', 'Non-Volatile Storage', shape='ellipse', style='filled', fillcolor=component_color)
dot.node('sd-card', 'SD Card Storage', shape='ellipse', style='filled', fillcolor=component_color)
dot.node('i2s', 'I2S Audio Output', shape='ellipse', style='filled', fillcolor=component_color)

# Define relationships between modules and components
dot.edge('main.c', 'alarm.c', label='Initializes')
dot.edge('main.c', 'network.c', label='Initializes')
dot.edge('main.c', 'display.c', label='Initializes')
dot.edge('main.c', 'sound.c', label='Initializes')
dot.edge('main.c', 'pot.c', label='Initializes')
dot.edge('main.c', 'storage.c', label='Initializes')

dot.edge('network.c', 'wifi', label='Uses')
dot.edge('network.c', 'sntp', label='Synchronizes')

dot.edge('display.c', 'e-paper', label='Controls')

dot.edge('sound.c', 'i2s', label='Uses')
dot.edge('sound.c', 'sd-card', label='Reads Files')

dot.edge('pot.c', 'nvs', label='Calibrates')

dot.edge('storage.c', 'sd-card', label='Manages')
dot.edge('storage.c', 'nvs', label='Uses')

# Add event-driven communication between modules
dot.edge('alarm.c', 'display.c', label='Event: Update Display')
dot.edge('alarm.c', 'sound.c', label='Event: Trigger Sound')
dot.edge('network.c', 'alarm.c', label='Event: Time Update')

# Render and save the graph to a file
dot.render('esp32_alarm_clock_architecture', view=False)