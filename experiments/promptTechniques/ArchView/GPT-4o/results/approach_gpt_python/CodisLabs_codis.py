from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Codis and Redis Architecture', format='png')

# Define nodes for Core Redis Components
dot.node('A', 'server.h', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('B', 'ae (Event Loop)', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('C', 'zmalloc (Memory Allocator)', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('D', 'rio (IO Stream Abstraction)', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('E', 'Networking.c', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('F', 'config.c', shape='rectangle', style='filled', fillcolor='lightblue')

# Define nodes for Extensibility & Integrations
dot.node('G', 'Lua Scripting', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('H', 'hiredis (Client Library)', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('I', 'redigo (Client Library)', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('J', 'Sentinel (High Availability)', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('K', 'Telemetry (StatsD, InfluxDB)', shape='rectangle', style='filled', fillcolor='lightgreen')

# Define nodes for Concurrency & Scalability
dot.node('L', 'Single-Threaded Model', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('M', 'Redis Cluster', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('N', 'Connection Pooling', shape='rectangle', style='filled', fillcolor='lightcoral')

# Define nodes for Memory Management & Allocators
dot.node('O', 'Jemalloc', shape='rectangle', style='filled', fillcolor='lightyellow')
dot.node('P', 'Thread Cache', shape='rectangle', style='filled', fillcolor='lightyellow')

# Define nodes for Error Handling and Testing
dot.node('Q', 'Testing Framework (Tcl)', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('R', 'Error Handling', shape='rectangle', style='filled', fillcolor='lightgrey')

# Define nodes for External Libraries and Modules
dot.node('S', 'Autoconf and Makefile', shape='rectangle', style='filled', fillcolor='lightpink')

# Define edges to represent data flow and dependencies
dot.edges(['AB', 'AC', 'AD', 'AE', 'AF'])
dot.edges(['AG', 'AH', 'AI', 'AJ', 'AK'])
dot.edges(['AL', 'AM', 'AN'])
dot.edges(['AO', 'AP'])
dot.edges(['AQ', 'AR'])
dot.edge('S', 'A', label='Configuration')

# Render the graph to a file
dot.render('codis_redis_architecture', view=True)