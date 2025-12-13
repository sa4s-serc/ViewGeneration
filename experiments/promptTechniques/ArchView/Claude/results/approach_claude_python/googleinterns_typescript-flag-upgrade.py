import graphviz

# Create a new directed graph
dot = graphviz.Digraph(comment='TypeScript Flag Upgrade Tool Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded', fontname='Arial')
dot.attr('edge', fontname='Arial', fontsize='10')

# Add main components with descriptions
dot.node('CLI', 'CLI Entry Point\n(src/index.ts)\nParses arguments & initiates upgrade', shape='component')
dot.node('Runner', 'Runner\n(src/runner.ts)\nOrchestrates upgrade process', shape='component')
dot.node('Parser', 'Parser\n(src/parser.ts)\nParses TypeScript project', shape='component')
dot.node('ErrorDetector', 'Error Detector\n(src/error_detectors/*.ts)\nDetects compiler errors', shape='component')
dot.node('Manipulator', 'Manipulator\n(src/manipulators/*.ts)\nApplies code fixes', shape='component')
dot.node('Emitter', 'Emitter\n(src/emitters/*.ts)\nWrites modified code', shape='component')
dot.node('Logger', 'Logger\n(src/loggers/*.ts)\nHandles message output', shape='component')
dot.node('Types', 'Types\n(src/types.ts)\nShared types & interfaces', shape='note')
dot.node('Utils', 'Utilities\n(src/util/*.ts)\nShared helper functions', shape='note')

# Create subgraph for plugin-based manipulators
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Plugin-based Manipulators', style='rounded', color='blue')
    c.node('NoImplicitReturns', 'NoImplicitReturns\nManipulator')
    c.node('StrictNullChecks', 'StrictNullChecks\nManipulator')
    c.node('NoImplicitAny', 'NoImplicitAny\nManipulator')
    
# Add relationships
dot.edge('CLI', 'Runner', 'creates')
dot.edge('Runner', 'Parser', 'uses')
dot.edge('Runner', 'ErrorDetector', 'uses')
dot.edge('Runner', 'Manipulator', 'uses')
dot.edge('Runner', 'Emitter', 'uses')
dot.edge('Runner', 'Logger', 'uses')
dot.edge('Parser', 'Types', 'uses')
dot.edge('ErrorDetector', 'Types', 'uses')
dot.edge('Manipulator', 'Types', 'uses')
dot.edge('Emitter', 'Types', 'uses')
dot.edge('Logger', 'Types', 'uses')
dot.edge('ErrorDetector', 'Utils', 'uses')
dot.edge('Manipulator', 'Utils', 'uses')
dot.edge('Parser', 'Utils', 'uses')

# Connect plugin manipulators
dot.edge('Manipulator', 'NoImplicitReturns', 'implements')
dot.edge('Manipulator', 'StrictNullChecks', 'implements')
dot.edge('Manipulator', 'NoImplicitAny', 'implements')

# Set graph attributes
dot.attr(fontname='Arial')
dot.attr(rankdir='TB')
dot.attr(splines='ortho')

# Render the graph
dot.render('typescript_flag_upgrade_architecture', format='png', cleanup=True)