from graphviz import Digraph

dot = Digraph(comment='FIFArm Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add components
dot.node('web', 'Web Interface\n(Thymeleaf)')
dot.node('controllers', 'Controllers\nPathController\nIndexController\nJsonController')
dot.node('services', 'Services\nHttpRequestService\nMongoService\nLogService')
dot.node('scheduler', 'Scheduler')
dot.node('db', 'MongoDB', shape='cylinder')
dot.node('fut_api', 'EA Sports FUT API', shape='cloud')
dot.node('logging', 'Logging\n(Logback)', shape='note')

# Add connections
dot.edge('web', 'controllers')
dot.edge('controllers', 'services')
dot.edge('services', 'db')
dot.edge('services', 'fut_api')
dot.edge('scheduler', 'services')
dot.edge('services', 'logging')

# Generate diagram
dot.render('fifarm_architecture', format='png', cleanup=True)