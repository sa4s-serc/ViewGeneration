import graphviz

dot = graphviz.Digraph(comment='ESP32 Alarm Clock Architecture')
dot.attr(rankdir='TB', size='8,10')

# Main components
with dot.subgraph(name='cluster_main') as c:
    c.attr(label='Main Application', style='filled', color='lightgrey')
    c.node('main', 'main.c', shape='ellipse')
    c.node('config', 'config.h', shape='rectangle')

# Core modules
with dot.subgraph(name='cluster_modules') as c:
    c.attr(label='Core Modules', style='filled', color='lightblue')
    c.node('alarm', 'alarm.c/h', shape='rectangle')
    c.node('network', 'network.c/h', shape='rectangle')
    c.node('display', 'display.c/h', shape='rectangle')
    c.node('sound', 'sound.c/h', shape='rectangle')
    c.node('pot', 'pot.c/h', shape='rectangle')
    c.node('storage', 'storage.c/h', shape='rectangle')

# External components
with dot.subgraph(name='cluster_external') as c:
    c.attr(label='External Components', style='filled', color='lightgreen')
    c.node('freertos', 'FreeRTOS', shape='ellipse')
    c.node('esp_idf', 'ESP-IDF', shape='ellipse')
    c.node('sdkconfig', 'sdkconfig', shape='rectangle')
    c.node('cmake', 'CMakeLists.txt', shape='rectangle')

# Hardware components
with dot.subgraph(name='cluster_hardware') as c:
    c.attr(label='Hardware', style='filled', color='lightyellow')
    c.node('wifi', 'WiFi', shape='ellipse')
    c.node('epaper', 'E-Paper Display', shape='ellipse')
    c.node('sd_card', 'SD Card', shape='ellipse')
    c.node('potentiometers', 'Potentiometers', shape='ellipse')
    c.node('buttons', 'Buttons/Switches', shape='ellipse')
    c.node('i2s', 'I2S Audio', shape='ellipse')

# Event-driven communication
dot.edge('main', 'alarm', label='initializes')
dot.edge('main', 'network', label='initializes')
dot.edge('main', 'display', label='initializes')
dot.edge('main', 'sound', label='initializes')
dot.edge('main', 'pot', label='initializes')
dot.edge('main', 'storage', label='initializes')

# Task queue patterns
dot.edge('alarm', 'display', label='alarm_time_queue', style='dashed')
dot.edge('alarm', 'sound', label='alarm_trigger', style='dashed')
dot.edge('network', 'display', label='time_updates', style='dashed')
dot.edge('pot', 'alarm', label='alarm_setting', style='dashed')

# Hardware interactions
dot.edge('network', 'wifi', label='connects', color='blue')
dot.edge('display', 'epaper', label='renders', color='blue')
dot.edge('sound', 'i2s', label='plays', color='blue')
dot.edge('storage', 'sd_card', label='reads/writes', color='blue')
dot.edge('pot', 'potentiometers', label='reads', color='blue')
dot.edge('alarm', 'buttons', label='interrupts', color='blue')

# Framework dependencies
dot.edge('main', 'freertos', label='uses', style='dotted')
dot.edge('main', 'esp_idf', label='uses', style='dotted')
dot.edge('main', 'sdkconfig', label='configures', style='dotted')
dot.edge('main', 'cmake', label='builds', style='dotted')

# Configuration dependencies
dot.edge('network', 'config', label='uses pins', style='dashed')
dot.edge('display', 'config', label='uses pins', style='dashed')
dot.edge('sound', 'config', label='uses pins', style='dashed')
dot.edge('pot', 'config', label='uses pins', style='dashed')
dot.edge('storage', 'config', label='uses pins', style='dashed')

dot.render('esp32_alarm_clock_architecture', format='png', cleanup=True)