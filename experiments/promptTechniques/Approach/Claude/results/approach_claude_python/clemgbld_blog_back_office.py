from graphviz import Digraph

dot = Digraph(comment='Blog Back Office Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add components
dot.node('UI', 'UI Layer\n(React Components)')
dot.node('Store', 'Redux Store\n(State Management)')
dot.node('Core', 'Core Layer\n(Use Cases, Entities)')
dot.node('Infrastructure', 'Infrastructure Layer\n(API, Storage)')

# Add external dependencies
dot.node('RichTextEditor', 'Rich Text Editor\n(Plate)')
dot.node('Router', 'React Router')
dot.node('API', 'External API')
dot.node('LocalStorage', 'Local Storage')

# Add connections
dot.edge('UI', 'Store', 'Actions/State')
dot.edge('Store', 'Core', 'Use Cases')
dot.edge('Core', 'Infrastructure', 'Ports')
dot.edge('Infrastructure', 'API', 'HTTP Calls')
dot.edge('Infrastructure', 'LocalStorage', 'Storage')
dot.edge('UI', 'RichTextEditor', 'Article Editing')
dot.edge('UI', 'Router', 'Navigation')

# Generate the diagram
dot.render('blog_architecture', format='png', cleanup=True)