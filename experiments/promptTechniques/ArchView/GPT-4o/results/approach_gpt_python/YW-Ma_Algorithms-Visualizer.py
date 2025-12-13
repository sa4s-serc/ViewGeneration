from graphviz import Digraph

dot = Digraph(comment='Algorithm Visualization Application')

# Frontend Components
dot.node('A', 'React Frontend')
dot.node('B', 'Map.js (Baidu Maps API)')
dot.node('C', 'GraphSVG.js')
dot.node('D', 'GraphTable.js')
dot.node('E', 'Sidebar.js')
dot.node('F', 'Panel.js')
dot.node('G', 'BodyInfo.js')
dot.node('H', 'HeadInfo.js')
dot.node('I', 'MyRoute.js')
dot.node('J', 'MainInterface.js')
dot.node('K', 'Reports.js')

# Backend Components
dot.node('L', 'Node.js Backend')
dot.node('M', 'Express.js')
dot.node('N', 'Algorithm Execution (C++ executables)')
dot.node('O', 'MySQL Database')
dot.node('P', 'eventProxy.js')

# Authentication
dot.node('Q', 'Authentication')
dot.node('R', 'Authorize.js')
dot.node('S', 'User.js')

# Relationships
dot.edges(['AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ', 'AK'])
dot.edges(['LM', 'LN', 'LO', 'LP'])
dot.edge('Q', 'R')
dot.edge('Q', 'S')
dot.edge('S', 'O')

# Styling
dot.attr('node', shape='rectangle')
dot.attr('edge', arrowhead='normal')

# Client-Server Communication
dot.edge('A', 'L', label='REST API', style='dashed')

# Event-Driven Communication
dot.edge('C', 'D', label='eventProxy.js', style='dotted')

# Database Connection
dot.edge('L', 'O', label='SQL Queries', style='dashed')

# Legend
dot.node('T', 'Legend', shape='plaintext')
dot.edge('T', 'A', label='Frontend Components')
dot.edge('T', 'L', label='Backend Components')
dot.edge('T', 'Q', label='Authentication & Authorization')

dot.render('algorithm_visualization_application', format='png', cleanup=True)