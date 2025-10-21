from graphviz import Digraph

dot = Digraph(comment='Koa.js Architecture')

# Nodes for the main components
dot.node('A', 'Client', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('B', 'Koa.js Server', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('C', 'Database (MongoDB)', shape='rectangle', style='filled', fillcolor='lightyellow')

# Nodes for subsystems within Koa.js Server
dot.node('D', 'Middleware Layer', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('E', 'Controller Layer', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('F', 'Model Layer', shape='rectangle', style='filled', fillcolor='lightgrey')

# Edges to represent communication
dot.edge('A', 'B', label='HTTP Requests')
dot.edge('B', 'D', label='Middleware Processing', style='dashed')
dot.edge('D', 'E', label='Route Handling', style='dashed')
dot.edge('E', 'F', label='Data Access', style='dashed')
dot.edge('F', 'C', label='CRUD Operations')

# Adding styles to represent architectural concerns
dot.attr(rankdir='LR', size='8,5')
dot.attr('node', shape='rectangle')
dot.attr('edge', arrowsize='0.7')

# Render the graph
dot.render('koa_js_architecture', format='png', cleanup=True)