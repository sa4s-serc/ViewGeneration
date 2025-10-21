from graphviz import Digraph

# Create a directed graph
dot = Digraph(comment='QAPM: Android Application Performance Monitoring Library')

# Set graph style and attributes
dot.attr('graph', rankdir='LR', layout='dot')
dot.attr('node', shape='box', style='filled', color='lightgrey')
dot.attr('edge', style='solid', arrowhead='vee')

# Define nodes
dot.node('A', 'QAPM Library (qapm-lib/)')
dot.node('B', 'QAPM Gradle Plugin (buildSrc/)')
dot.node('C', 'README.md')
dot.node('D', 'QAPM.java')
dot.node('E', 'Tracing')
dot.node('F', 'DAO')
dot.node('G', 'Network')
dot.node('H', 'Plugin Interfaces')
dot.node('I', 'QBuildPlugin.groovy')
dot.node('J', 'AspectJAppTransform.groovy')
dot.node('K', 'qapm-sample/')

# Define edges
dot.edge('A', 'D', label='Core Component')
dot.edge('A', 'E', label='Performance Metrics')
dot.edge('A', 'F', label='Data Storage')
dot.edge('A', 'G', label='Network Instrumentation')
dot.edge('A', 'H', label='Lifecycle Methods')
dot.edge('B', 'I', label='Entry Point')
dot.edge('B', 'J', label='Transform API')
dot.edge('D', 'E', label='Monitors Performance')
dot.edge('D', 'F', label='Manages Data')
dot.edge('D', 'G', label='Interception')
dot.edge('D', 'H', label='Triggers Tracers')
dot.edge('K', 'A', label='Demonstrates Usage')

# Render the diagram
dot.render('qapm_architecture_diagram', format='png', cleanup=True)
