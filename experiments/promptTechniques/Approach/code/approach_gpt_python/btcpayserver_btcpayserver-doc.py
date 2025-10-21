from graphviz import Digraph

dot = Digraph(comment='BTCPay Server Documentation Architecture')

# Define nodes
dot.node('U', 'User Guides')
dot.node('D', 'Deployment Documentation')
dot.node('Dev', 'Development Documentation')
dot.node('API', 'API Integration')
dot.node('T', 'Troubleshooting and FAQ')
dot.node('Th', 'Theming')

dot.node('V', 'VuePress')
dot.node('C', 'Core Documentation')
dot.node('B', 'Build & Deployment')
dot.node('Config', 'Configuration')
dot.node('Theme', 'Theme')
dot.node('Util', 'Utilities')

dot.node('M', 'Modular Design')
dot.node('A', 'API-Centric')
dot.node('P', 'Plugin Architecture')
dot.node('Micro', 'Microservices')
dot.node('Docker', 'Docker-Based Deployment')

# Define edges
dot.edge('U', 'V', 'Built with')
dot.edge('D', 'V', 'Built with')
dot.edge('Dev', 'V', 'Built with')
dot.edge('API', 'V', 'Built with')
dot.edge('T', 'V', 'Built with')
dot.edge('Th', 'V', 'Built with')

dot.edge('V', 'C', 'Contains')
dot.edge('V', 'B', 'Contains')
dot.edge('V', 'Config', 'Contains')
dot.edge('V', 'Theme', 'Contains')
dot.edge('V', 'Util', 'Contains')

dot.edge('C', 'M', 'Highlights')
dot.edge('C', 'A', 'Highlights')
dot.edge('C', 'P', 'Highlights')
dot.edge('C', 'Micro', 'Suggests')
dot.edge('C', 'Docker', 'Emphasizes')

# Render the diagram
dot.format = 'png'
dot.render('btcpay_documentation_architecture')