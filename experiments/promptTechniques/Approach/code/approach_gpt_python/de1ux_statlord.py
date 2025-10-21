from graphviz import Digraph

dot = Digraph(comment='Statlord Dashboard Architecture')

# Client-Server Architecture
dot.attr(rankdir='LR', size='8,5')

# Client Components
dot.node('A', 'Dashboard Editor\n(React, Redux, Fabric.js)')
dot.node('B', 'Data Visualization\n(Gauges)')
dot.node('C', 'Display Management\n(Raspberry Pi, Arduino, Browsers)')

# Server Components
dot.node('D', 'Layout Management\n(Django REST Framework)')
dot.node('E', 'Data Streaming\n(API Endpoints)')
dot.node('F', 'Display Rendering\n(Viewers)')
dot.node('G', 'API\n(HTTP-based, Django)')

# Supporting Scripts
dot.node('H', 'Scripts\n(clock_and_temp.py, inky.py)')

# Connections - Client to Server
dot.edge('A', 'D', label='Create/Edit Layouts')
dot.edge('B', 'E', label='Request Data')
dot.edge('C', 'F', label='Register Displays')

# Connections - Server to Client
dot.edge('D', 'A', label='Send Layouts')
dot.edge('E', 'B', label='Stream Data')
dot.edge('F', 'C', label='Render Content')

# API Connections
dot.edge('G', 'D', label='Manage Layouts')
dot.edge('G', 'E', label='Manage Data')
dot.edge('G', 'F', label='Manage Displays')

# Supporting Scripts Connections
dot.edge('H', 'E', label='Mock Data Generation')
dot.edge('H', 'F', label='Display Integration')

# Docker and Configuration
dot.node('I', 'Docker & Config\n(Dockerfile, Makefile)')
dot.edge('I', 'D', label='Containerize')
dot.edge('I', 'G', label='Containerize')

# Legend
dot.node('J', 'Legend:\nSquares: Components\nArrows: Data Flow')
dot.attr('node', shape='square')
dot.edge('J', 'A', style='invis')

dot.render('statlord_dashboard_architecture', format='png', cleanup=True)