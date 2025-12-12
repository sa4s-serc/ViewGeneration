import graphviz

# Create a new directed graph
dot = graphviz.Digraph('Nobel Prize Laureates Architecture')
dot.attr(rankdir='TB')

# Define node attributes
dot.attr('node', shape='rectangle', style='rounded', fontname='Arial', fontsize='10')
dot.attr('edge', fontname='Arial', fontsize='8')

# Create clusters/subgraphs
with dot.subgraph(name='cluster_0') as frontend:
    frontend.attr(label='Frontend Layer', style='rounded', color='lightblue')
    frontend.node('html', 'index.html\nUser Interface')
    frontend.node('css', 'main.css\nStyling')
    frontend.node('js', 'main.js\nFront-end Logic\nEvent Handling')
    
with dot.subgraph(name='cluster_1') as backend:
    backend.attr(label='Backend Layer', style='rounded', color='lightgreen')
    backend.node('server', 'server.js\nNode.js Server')
    backend.node('router', 'router.js\nRequest Routing')
    backend.node('handler', 'handler.js\nRequest Handling')
    backend.node('algorithm', 'algorithm.js\nAutocomplete Logic')
    backend.node('data', 'data.json\nLaureates Data')

with dot.subgraph(name='cluster_2') as testing:
    testing.attr(label='Testing Layer', style='rounded', color='lightpink')
    testing.node('qunit', 'qunit.html\nQUnit Testing')
    testing.node('frontend_test', 'frontendTests.js')
    testing.node('backend_test', 'backendTests.js')

# Add edges to show relationships
# Frontend relationships
dot.edge('html', 'css', 'styles')
dot.edge('html', 'js', 'scripts')
dot.edge('js', 'server', 'API requests')

# Backend relationships
dot.edge('server', 'router', 'routes')
dot.edge('router', 'handler', 'handle requests')
dot.edge('handler', 'algorithm', 'process')
dot.edge('algorithm', 'data', 'query')

# Testing relationships
dot.edge('frontend_test', 'js', 'tests')
dot.edge('backend_test', 'algorithm', 'tests')
dot.edge('qunit', 'frontend_test', 'runs')

# Set graph title
dot.attr(label='Nobel Prize Laureates Autocomplete Architecture\nArchitectural View')

# Save the diagram
dot.render('nobel_architecture', format='png', cleanup=True)