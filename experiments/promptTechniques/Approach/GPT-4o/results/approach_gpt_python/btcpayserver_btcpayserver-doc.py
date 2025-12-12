from graphviz import Digraph

dot = Digraph(comment='BTCPay Server Documentation Architecture')

# Define nodes
dot.node('A', 'VuePress', shape='rectangle')
dot.node('B', 'User Guides', shape='rectangle')
dot.node('C', 'Deployment Documentation', shape='rectangle')
dot.node('D', 'Development Documentation', shape='rectangle')
dot.node('E', 'API Integration', shape='rectangle')
dot.node('F', 'Troubleshooting and FAQ', shape='rectangle')
dot.node('G', 'Theming', shape='rectangle')
dot.node('H', 'Docker', shape='rectangle')
dot.node('I', 'API', shape='rectangle')
dot.node('J', 'Plugin Architecture', shape='rectangle')

# Define edges
dot.edge('A', 'B', label='contains')
dot.edge('A', 'C', label='contains')
dot.edge('A', 'D', label='contains')
dot.edge('A', 'E', label='contains')
dot.edge('A', 'F', label='contains')
dot.edge('A', 'G', label='contains')
dot.edge('C', 'H', label='uses')
dot.edge('D', 'I', label='provides')
dot.edge('D', 'J', label='extends')

# Render diagram
dot.render('btcpay_architecture_diagram', format='png', cleanup=True)