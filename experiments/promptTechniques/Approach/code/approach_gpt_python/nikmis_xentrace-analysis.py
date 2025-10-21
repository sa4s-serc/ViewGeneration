from graphviz import Digraph

dot = Digraph(comment='Xen Performance Analysis Tool')

# Set graph attributes
dot.attr(rankdir='TB', size='10,8')

# Components
dot.node('A', 'Xentrace-analysis.c', shape='rectangle')
dot.node('B', 'Reader', shape='rectangle')
dot.node('C', 'EventHandler', shape='rectangle')
dot.node('D', 'Event', shape='rectangle')
dot.node('E', 'Trace.h', shape='rectangle')
dot.node('F', 'List.h', shape='rectangle')
dot.node('G', 'CPU Utilization', shape='rectangle')
dot.node('H', 'CPU Scheduling Latency', shape='rectangle')
dot.node('I', 'Time in Hypervisor', shape='rectangle')
dot.node('J', 'Disk I/O', shape='rectangle')
dot.node('K', 'Xen Event Statistics', shape='rectangle')
dot.node('L', 'Trap Counting', shape='rectangle')
dot.node('M', 'examples/*', shape='rectangle')

# Subsystems
dot.node('N', 'Analysis Tools', shape='cylinder')
dot.node('O', 'Core Components', shape='cylinder')

# Grouping components into subsystems
dot.edge('O', 'A')
dot.edge('O', 'B')
dot.edge('O', 'C')
dot.edge('O', 'D')
dot.edge('O', 'E')
dot.edge('O', 'F')

dot.edge('N', 'G')
dot.edge('N', 'H')
dot.edge('N', 'I')
dot.edge('N', 'J')
dot.edge('N', 'K')
dot.edge('N', 'L')

# Connectors
dot.edge('A', 'B', label='Initiates & Manages')
dot.edge('B', 'C', label='Parses & Distributes')
dot.edge('C', 'D', label='Handles Events')
dot.edge('D', 'E', label='Uses Trace IDs')
dot.edge('D', 'F', label='Manages Handlers')

# Analysis Tools
dot.edge('A', 'M', label='Executes specific tool')
dot.edge('M', 'G', label='CPU Analysis')
dot.edge('M', 'H', label='Scheduling Analysis')
dot.edge('M', 'I', label='Time Analysis')
dot.edge('M', 'J', label='I/O Analysis')
dot.edge('M', 'K', label='Event Stats')
dot.edge('M', 'L', label='Custom Analysis')

# Styles for non-functional requirements
dot.attr('node', shape='rect', style='filled', color='lightgrey')
dot.node('P', 'Event-Driven Architecture', shape='rectangle')

# Display diagram
dot.view()