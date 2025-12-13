import graphviz as gv

# Create a new directed graph
dot = gv.Digraph(comment='Solenya Framework Architecture')
dot.attr(rankdir='TB')

# Add nodes for main components
dot.node('Component', 'Component\n(Base Class)', shape='box')
dot.node('App', 'App\n(Entry Point)', shape='box')
dot.node('Router', 'Router', shape='box')
dot.node('Validator', 'Validator', shape='box')
dot.node('Storage', 'Storage', shape='box')
dot.node('TimeTravel', 'TimeTravel', shape='box')
dot.node('VirtualDOM', 'Virtual DOM', shape='box')
dot.node('HTML', 'HTML Helpers', shape='box')
dot.node('Widgets', 'Widgets', shape='box')

# Add edges with relationships
dot.edge('App', 'Component', 'manages')
dot.edge('Component', 'VirtualDOM', 'uses')
dot.edge('Component', 'HTML', 'uses')
dot.edge('Component', 'Widgets', 'uses')
dot.edge('App', 'Router', 'contains')
dot.edge('App', 'Storage', 'manages')
dot.edge('App', 'TimeTravel', 'enables')
dot.edge('Component', 'Validator', 'uses')
dot.edge('Storage', 'TimeTravel', 'supports')

# Set graph attributes
dot.attr(fontsize='10')
dot.attr('node', shape='box', style='rounded')
dot.attr('edge', fontsize='10')

# Save the diagram
dot.render('solenya_architecture', format='png', cleanup=True)