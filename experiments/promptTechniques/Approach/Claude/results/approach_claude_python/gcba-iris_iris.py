from graphviz import Digraph

dot = Digraph(comment='Iris IoT Backend Architecture')
dot.attr(rankdir='TB', splines='ortho')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded', fontname='Arial')

# Add components
dot.node('dock', 'Dock\n(Message Listener)')
dot.node('dispatcher', 'Dispatcher\n(Central Router)')
dot.node('handler', 'Handler\n(Data Processor)')
dot.node('hook', 'Hook\n(Custom Logic)')
dot.node('thread_pool', 'Thread Pool')
dot.node('flow', 'Flow\n(Pipeline Definition)')
dot.node('cli', 'CLI Tool')
dot.node('logger', 'Logger\n(Winston)')
dot.node('validator', 'Validator\n(PropChecker)')

# Add edges
dot.edge('dock', 'dispatcher', 'Messages')
dot.edge('dispatcher', 'handler', 'Process Data')
dot.edge('handler', 'hook', 'Pre/Post Processing')
dot.edge('dispatcher', 'thread_pool', 'Parallel Execution')
dot.edge('flow', 'dispatcher', 'Defines Pipeline')
dot.edge('cli', 'flow', 'Manages')
dot.edge('logger', 'dispatcher', 'Logs')
dot.edge('validator', 'flow', 'Validates')
dot.edge('hook', 'dispatcher', 'Returns')

# Set graph attributes
dot.attr(fontsize='20')
dot.attr(label='Iris Framework Architecture\nPlugin-based IoT Backend')

# Render the diagram
dot.render('iris_architecture', format='png', cleanup=True)