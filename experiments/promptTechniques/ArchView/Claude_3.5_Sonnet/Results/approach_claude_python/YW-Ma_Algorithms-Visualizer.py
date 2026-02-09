import graphviz

# Create digraph
dot = graphviz.Digraph(comment='Algorithm Visualization Application Architecture')
dot.attr(rankdir='TB')

# Styling
dot.attr('node', shape='box', style='rounded')
dot.attr(compound='true')
dot.attr(splines='ortho')

# Frontend cluster
with dot.subgraph(name='cluster_frontend') as frontend:
    frontend.attr(label='Frontend', style='rounded', color='blue')
    frontend.node('map_js', 'Map.js\n(BMap Integration)')
    frontend.node('graph_svg', 'GraphSVG.js\n(Visualization)')
    frontend.node('graph_table', 'GraphTable.js\n(Data View)')
    frontend.node('sidebar', 'Sidebar.js\n(Controls)')
    frontend.node('panel', 'Panel.js')
    frontend.node('route', 'MyRoute.js\n(Routing)')
    frontend.node('event', 'eventProxy.js')
    
    # Frontend component relationships
    frontend.edge('panel', 'graph_svg')
    frontend.edge('panel', 'graph_table')
    frontend.edge('sidebar', 'panel')
    frontend.edge('event', 'graph_svg')
    frontend.edge('event', 'graph_table')
    frontend.edge('route', 'panel')

# Backend cluster
with dot.subgraph(name='cluster_backend') as backend:
    backend.attr(label='Backend', style='rounded', color='green')
    backend.node('express', 'Express.js\nServer')
    backend.node('auth', 'Authentication\nModule')
    backend.node('algo', 'Algorithm\nExecutor')
    backend.node('db_access', 'Database\nAccess Layer')

    # Backend component relationships
    backend.edge('express', 'auth')
    backend.edge('express', 'algo')
    backend.edge('express', 'db_access')

# External systems
dot.node('db', 'MySQL', shape='cylinder')
dot.node('cpp', 'C++ Algorithm\nExecutables', shape='component')

# Cross-component relationships
dot.edge('map_js', 'express', 'REST API')
dot.edge('graph_svg', 'express', 'REST API')
dot.edge('graph_table', 'express', 'REST API')
dot.edge('sidebar', 'express', 'REST API')
dot.edge('algo', 'cpp', 'Execution')
dot.edge('db_access', 'db', 'SQL')

# Save diagram
dot.render('architecture', format='png', cleanup=True)