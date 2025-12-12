from graphviz import Digraph

def generate_architecture_diagram():
    dot = Digraph(comment='EMonitor Project ESP32 Device-Side Implementation')

    # Define nodes
    dot.node('ESP32', 'ESP32 Device', shape='rect', style='filled', fillcolor='lightblue')
    dot.node('Sensors', 'Sensors\n(DHT11, BMP180/BMP085, LDR)', shape='rect', style='filled', fillcolor='lightgreen')
    dot.node('Buffer', 'Data Buffer', shape='rect', style='filled', fillcolor='lightgray')
    dot.node('WiFi', 'WiFi Module', shape='rect', style='filled', fillcolor='lightyellow')
    dot.node('Server', 'Backend Server', shape='rect', style='filled', fillcolor='orange')
    dot.node('Display', 'OLED Display', shape='rect', style='filled', fillcolor='lightpink')
    dot.node('Email', 'Email Alerts\n(SMTP)', shape='rect', style='filled', fillcolor='lightcoral')

    # Define edges
    dot.edge('Sensors', 'ESP32', label='Read Data', arrowhead='normal')
    dot.edge('ESP32', 'Buffer', label='Buffer Data', arrowhead='normal')
    dot.edge('Buffer', 'WiFi', label='Push/Pop Data', arrowhead='normal')
    dot.edge('WiFi', 'Server', label='HTTP POST', arrowhead='normal')
    dot.edge('ESP32', 'Display', label='Update Display', arrowhead='normal')
    dot.edge('ESP32', 'Email', label='Send Alerts', arrowhead='normal')

    # Add legend
    dot.node('Legend', 'Legend:\nRectangles: Components', shape='note', fontsize='10')

    # Save and render the diagram
    dot.render('architecture_diagram', format='png', cleanup=True)

generate_architecture_diagram()