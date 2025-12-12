from graphviz import Digraph

dot = Digraph(comment='Resurgence VM Architecture')

# Define styles
dot.attr('node', shape='rectangle', style='filled', color='lightgrey')
dot.attr('edge', style='solid')

# Core Components
dot.node('A', 'Virtual Machine Core')
dot.node('B', 'Bytecode Handling')
dot.node('C', 'Foreign Function Interface (FFI)')
dot.node('D', 'Instruction Set')
dot.node('E', 'Error Handling')
dot.node('F', 'Code Generation')

# Key Files and Roles
dot.node('G', 'Project Definition')
dot.node('H', 'Licensing & Documentation')
dot.node('I', 'Continuous Integration')
dot.node('J', 'Entry Point')
dot.node('K', 'External Function Interaction')
dot.node('L', 'Internal Implementation')
dot.node('M', 'Data Structures')
dot.node('N', 'FFI Implementation')

# Relationships
dot.edge('A', 'B', label='Reads/Writes Bytecode')
dot.edge('A', 'C', label='Interacts via FFI')
dot.edge('A', 'D', label='Executes Instructions')
dot.edge('A', 'E', label='Handles Errors')
dot.edge('A', 'F', label='Generates Code')

dot.edge('G', 'J', label='Defines Entry Point')
dot.edge('K', 'L', label='Interacts with VM')
dot.edge('L', 'M', label='Uses Data Structures')
dot.edge('C', 'N', label='Implements FFI')

# Additional Metadata
dot.attr(label='Resurgence VM Architectural View\nRegister-Based, Embeddable, Modular', fontsize='20', fontcolor='blue')
dot.attr('graph', layout='dot', rankdir='TB')

# Render the diagram
dot.render('resurgence_vm_architecture', format='png', cleanup=True)