from graphviz import Digraph

dot = Digraph(comment='ESP32 Alarm Clock Architecture')

# Components
dot.node('A', 'main.c: Main Application')
dot.node('B', 'alarm.c/h: Alarm Logic')
dot.node('C', 'network.c/h: Network Management')
dot.node('D', 'display.c/h: Display Control')
dot.node('E', 'sound.c/h: Sound Management')
dot.node('F', 'pot.c/h: Potentiometer Handling')
dot.node('G', 'storage.c/h: Storage Management')
dot.node('H', 'config.h: Configuration')
dot.node('I', 'sdkconfig: ESP-IDF Config')
dot.node('J', 'CMakeLists.txt: Build Config')

# Relationships
dot.edges(['AB', 'AC', 'AD', 'AE', 'AF', 'AG'])
dot.edge('B', 'E', label='Trigger Sound')
dot.edge('C', 'A', label='WiFi & Time Sync')
dot.edge('D', 'A', label='Update Display')
dot.edge('F', 'B', label='Set Alarm Time')
dot.edge('G', 'A', label='Manage Files & NVS')
dot.edge('H', 'A', label='Project Config')
dot.edge('I', 'A', label='Build-time Config')
dot.edge('J', 'A', label='Build System')

# Style and Attributes
dot.attr(rankdir='LR', size='10')
dot.attr('node', shape='box', style='filled', color='lightblue')
dot.attr('edge', color='black')

dot.render('esp32_alarm_clock_architecture', format='png', cleanup=True)