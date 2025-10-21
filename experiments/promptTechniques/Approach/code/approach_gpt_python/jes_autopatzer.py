from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Autopatzer Project Architecture')

# Add nodes for each layer and components
dot.node('HW', 'Hardware Layer')
dot.node('LLC', 'Low-Level Control (Arduino)')
dot.node('COM', 'Communication (Perl)')
dot.node('UI', 'User Interface (JavaScript/Electron)')
dot.node('API', 'Lichess API')

# Add sub-components for hardware
dot.node('MC', 'Teensy 3.2 Microcontroller', shape='rect')
dot.node('SM', 'A4988 Stepper Motor Driver', shape='rect')
dot.node('MOSFET', 'IRF540N MOSFET', shape='rect')
dot.node('MUX', 'CD4051B Analog Multiplexer', shape='rect')

# Add sub-components for User Interface
dot.node('React', 'React-based UI', shape='rect')
dot.node('Electron', 'Electron app', shape='rect')
dot.node('Lichess', 'Lichess API Client', shape='rect')

# Add edges between components to show communication
dot.edge('HW', 'LLC', label='Control Signals')
dot.edge('LLC', 'COM', label='Analog Signal Processing')
dot.edge('COM', 'UI', label='Data Transmission')
dot.edge('UI', 'API', label='API Requests')
dot.edge('React', 'Electron', label='UI Management')
dot.edge('Electron', 'Lichess', label='Game Management')

# Add connections within Hardware layer
dot.edge('MC', 'SM', label='Motor Control')
dot.edge('MC', 'MOSFET', label='Load Switching')
dot.edge('MC', 'MUX', label='Sensor Input')

# Render the graph to a file and save it
dot.render('autopatzer_architecture', format='png', cleanup=True)