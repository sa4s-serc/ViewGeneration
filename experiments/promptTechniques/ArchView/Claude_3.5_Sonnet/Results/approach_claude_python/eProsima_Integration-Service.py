from graphviz import Digraph

dot = Digraph(comment='Software Architecture View')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded')

# Create main components
dot.node('json_lib', 'JSON Library\n(basic_json)')
dot.node('int_service', 'Integration Service')

# Core components of JSON Library
dot.node('parser', 'Parser')
dot.node('lexer', 'Lexer')
dot.node('sax', 'SAX Interface')
dot.node('io_adapters', 'I/O Adapters')
dot.node('binary_formats', 'Binary Formats\n(CBOR, MessagePack,\nUBJSON, BSON)')

# Core components of Integration Service
dot.node('core', 'Core Library')
dot.node('sys_handles', 'System Handles')
dot.node('config_parser', 'Configuration Parser')
dot.node('converter', 'Data Converter')

# Relationships for JSON Library
dot.edge('json_lib', 'parser')
dot.edge('json_lib', 'lexer')
dot.edge('json_lib', 'sax')
dot.edge('json_lib', 'io_adapters')
dot.edge('json_lib', 'binary_formats')
dot.edge('lexer', 'parser')

# Relationships for Integration Service
dot.edge('int_service', 'core')
dot.edge('int_service', 'sys_handles')
dot.edge('int_service', 'config_parser')
dot.edge('int_service', 'converter')
dot.edge('converter', 'json_lib', 'uses for\ndata conversion')

# Add subgraph for middleware connections
with dot.subgraph(name='cluster_middleware') as c:
    c.attr(label='Middleware Systems')
    c.node('fastdds', 'Fast DDS')
    c.node('ros', 'ROS 1/2')
    c.node('websocket', 'WebSocket')
    c.node('fiware', 'FIWARE')

# Connect System Handles to middleware
dot.edge('sys_handles', 'fastdds')
dot.edge('sys_handles', 'ros')
dot.edge('sys_handles', 'websocket')
dot.edge('sys_handles', 'fiware')

dot.render('architecture_view', format='png', cleanup=True)