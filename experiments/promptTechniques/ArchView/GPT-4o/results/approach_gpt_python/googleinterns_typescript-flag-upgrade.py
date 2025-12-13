from graphviz import Digraph

# Create a Digraph object
dot = Digraph(comment='TypeScript Flag Upgrade Tool Architecture')

# Set graph attributes for box and arrows style
dot.attr('node', shape='box', style='filled', color='lightgrey')
dot.attr('edge', arrowhead='open', arrowsize='1.0')

# Define nodes for core components
dot.node('CLI', 'CLI (src/index.ts)')
dot.node('Runner', 'Runner (src/runner.ts)')
dot.node('Parser', 'Parser (src/parser.ts)')
dot.node('Manipulator', 'Manipulator (src/manipulators/*.ts)')
dot.node('ErrorDetector', 'ErrorDetector (src/error_detectors/*.ts)')
dot.node('Emitter', 'Emitter (src/emitters/*.ts)')
dot.node('Logger', 'Logger (src/loggers/*.ts)')
dot.node('Util', 'Util (src/util/*.ts)')
dot.node('Tests', 'Tests (test/**/*_test.ts)')

# Define edges to represent interactions
dot.edge('CLI', 'Runner', label='initiates')
dot.edge('Runner', 'Parser', label='uses')
dot.edge('Runner', 'ErrorDetector', label='uses')
dot.edge('Runner', 'Manipulator', label='uses')
dot.edge('Runner', 'Emitter', label='uses')
dot.edge('Runner', 'Logger', label='uses')
dot.edge('Manipulator', 'Util', label='uses')
dot.edge('ErrorDetector', 'Util', label='uses')
dot.edge('Tests', 'CLI', label='tests')
dot.edge('Tests', 'Runner', label='tests')
dot.edge('Tests', 'Parser', label='tests')
dot.edge('Tests', 'Manipulator', label='tests')
dot.edge('Tests', 'ErrorDetector', label='tests')
dot.edge('Tests', 'Emitter', label='tests')
dot.edge('Tests', 'Logger', label='tests')

# Render the diagram to a file
dot.render('typescript_flag_upgrade_tool_architecture', format='png', cleanup=True)