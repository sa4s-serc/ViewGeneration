from graphviz import Digraph

dot = Digraph(comment='OpenHub Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add components
dot.node('crawler', 'GitHub Crawler\n(crawler.py)')
dot.node('rabbitmq', 'RabbitMQ\nMessage Queue')
dot.node('worker', 'Worker Manager\n(manager.py)')
dot.node('mongodb', 'MongoDB\nDatabase')

# Add analysis modules
with dot.subgraph(name='cluster_analysis') as c:
    c.attr(label='Analysis Modules')
    c.node('security', 'Security Analysis')
    c.node('testability', 'Testability Analysis')
    c.node('reusability', 'Reusability Analysis')
    c.node('usability', 'Usability Analysis')

# Add connections
dot.edge('crawler', 'rabbitmq', 'Publish Tasks')
dot.edge('rabbitmq', 'worker', 'Consume Tasks')
dot.edge('worker', 'security', 'Analyze')
dot.edge('worker', 'testability', 'Analyze')
dot.edge('worker', 'reusability', 'Analyze')
dot.edge('worker', 'usability', 'Analyze')
dot.edge('security', 'mongodb', 'Store Results')
dot.edge('testability', 'mongodb', 'Store Results')
dot.edge('reusability', 'mongodb', 'Store Results')
dot.edge('usability', 'mongodb', 'Store Results')
dot.edge('crawler', 'mongodb', 'Store Metadata')

# Render the diagram
dot.render('openhub_architecture', format='png', cleanup=True)