from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Algorithm Visualization Application Architecture')

# Define nodes for frontend components
dot.node('F1', 'React Frontend')
dot.node('F2', 'Map.js (Baidu Maps API)', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('F3', 'GraphSVG.js', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('F4', 'GraphTable.js', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('F5', 'Sidebar.js', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('F6', 'Panel.js', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('F7', 'MainInterface.js', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('F8', 'Reports.js', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('F9', 'react-router-dom', shape='rectangle', style='filled', fillcolor='lightblue')

# Define nodes for backend components
dot.node('B1', 'Node.js Backend')
dot.node('B2', 'Express.js', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('B3', 'C++ Executables\n(DFS, Dijkstra)', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('B4', 'MySQL Database', shape='cylinder', style='filled', fillcolor='lightcoral')
dot.node('B5', 'express-mysql-session', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('B6', 'eventProxy.js', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('B7', 'cluster', shape='rectangle', style='filled', fillcolor='lightcoral')

# Define nodes for authentication components
dot.node('A1', 'Authentication')
dot.node('A2', 'Authorize.js', shape='rectangle', style='filled', fillcolor='lightyellow')
dot.node('A3', 'User.js', shape='rectangle', style='filled', fillcolor='lightyellow')

# Define connections between components
dot.edge('F1', 'F2')
dot.edge('F1', 'F3')
dot.edge('F1', 'F4')
dot.edge('F1', 'F5')
dot.edge('F1', 'F6')
dot.edge('F6', 'F3')
dot.edge('F6', 'F4')
dot.edge('F1', 'F7')
dot.edge('F1', 'F8')
dot.edge('F1', 'F9')
dot.edge('B1', 'B2')
dot.edge('B1', 'B3')
dot.edge('B1', 'B4')
dot.edge('B4', 'B5')
dot.edge('B1', 'B6')
dot.edge('B1', 'B7')
dot.edge('A1', 'A2')
dot.edge('A1', 'A3')
dot.edge('F1', 'B1', label='API Calls', style='dashed')
dot.edge('F9', 'F7', label='Routing', style='dashed')
dot.edge('B2', 'B3', label='External Process\nInvocation', style='dashed')
dot.edge('B2', 'B4', label='Data Persistence', style='dashed')
dot.edge('A2', 'A3', label='Middleware', style='dashed')

# Define styles for the graph
dot.attr(rankdir='LR', size='10,5')

# Render the graph to a file
dot.render('algorithm_visualization_architecture', view=True)