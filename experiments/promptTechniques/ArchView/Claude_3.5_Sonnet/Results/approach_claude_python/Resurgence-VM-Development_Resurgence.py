from graphviz import Digraph

dot = Digraph(comment='Resurgence VM Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded')

# Add main components
dot.node('vm_core', 'Virtual Machine Core\n(Interpreter, Execution Engine)')
dot.node('bytecode', 'Bytecode Handler')
dot.node('ffi', 'FFI Interface')
dot.node('instruction', 'Instruction Set')
dot.node('error', 'Error Handling')
dot.node('codegen', 'Code Generation')

# Add subcomponents
dot.node('memory', 'Memory Management\n(Stack, Registers, Constants)')
dot.node('execution', 'Execution Engine')
dot.node('interpreter', 'Interpreter')
dot.node('reader', 'Code Reader')
dot.node('writer', 'Code Writer')
dot.node('native', 'Native Functions')
dot.node('error_context', 'Error Context')

# Define relationships
dot.edge('vm_core', 'memory')
dot.edge('vm_core', 'execution')
dot.edge('vm_core', 'interpreter')
dot.edge('bytecode', 'reader')
dot.edge('bytecode', 'writer')
dot.edge('ffi', 'native')
dot.edge('error', 'error_context')
dot.edge('execution', 'instruction')
dot.edge('interpreter', 'instruction')
dot.edge('native', 'interpreter')
dot.edge('codegen', 'bytecode')

# Render the diagram
dot.render('resurgence_vm_architecture', view=True, format='png')