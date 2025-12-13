from graphviz import Digraph

dot = Digraph(comment='Budget App Architecture')

# Define nodes
dot.node('A', 'index.html')
dot.node('B', 'index.php')
dot.node('C', 'README.md')
dot.node('D', 'script.js')
dot.node('E', 'style.css')

# Define subnodes in script.js
dot.node('D1', 'budgetController', shape='rect', style='filled', color='lightblue')
dot.node('D2', 'UIController', shape='rect', style='filled', color='lightgreen')
dot.node('D3', 'controller', shape='rect', style='filled', color='lightcoral')

# Define edges
dot.edge('A', 'D', 'links')
dot.edge('A', 'E', 'links')
dot.edge('B', 'A', 'redirects')
dot.edge('D', 'D1', 'manages data')
dot.edge('D', 'D2', 'handles UI')
dot.edge('D', 'D3', 'connects modules')

# Define relationships within script.js
dot.edge('D1', 'D3', 'provides data to')
dot.edge('D2', 'D3', 'updates UI via')

# Generate and render the diagram
dot.render('budget_app_architecture', format='png', cleanup=True)