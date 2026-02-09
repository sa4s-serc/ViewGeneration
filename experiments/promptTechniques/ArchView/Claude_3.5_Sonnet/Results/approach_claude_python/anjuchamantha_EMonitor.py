from graphviz import Digraph

dot = Digraph(comment='EMonitor ESP32 Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add main components
dot.node('sensors', 'Sensor Layer\n(DHT11, BMP180, LDR)')
dot.node('readings', 'Data Acquisition\n& Processing')
dot.node('buffer', 'Data Buffer\nQueue-based Storage')
dot.node('network', 'Network Layer\nWiFi Management')
dot.node('xml', 'Data Formatting\nXML Generation')
dot.node('display', 'Local Display\nOLED Interface')
dot.node('alert', 'Alert System\nEmail Notifications')
dot.node('server', 'Backend Server')

# Add edges with descriptions
dot.edge('sensors', 'readings', 'Raw Data')
dot.edge('readings', 'buffer', 'Processed Readings')
dot.edge('buffer', 'xml', 'Buffered Data')
dot.edge('xml', 'network', 'CAP-formatted XML')
dot.edge('network', 'server', 'HTTP POST')
dot.edge('readings', 'display', 'Sensor Values')
dot.edge('readings', 'alert', 'Temperature\nThreshold Check')
dot.edge('alert', 'network', 'SMTP')

# Add subgraph for local components
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='ESP32 Device')
    c.attr('node', shape='rectangle')
    c.node('readings')
    c.node('buffer')
    c.node('xml')
    c.node('network')
    c.node('display')
    c.node('alert')

# Render the diagram
dot.render('emonitor_architecture', view=True, format='png')