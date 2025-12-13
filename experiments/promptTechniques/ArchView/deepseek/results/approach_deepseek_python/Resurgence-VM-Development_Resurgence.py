import graphviz

dot = graphviz.Digraph(comment='Resurgence VM Architecture')
dot.attr(rankdir='TB', size='8,10')

with dot.subgraph(name='cluster_vm_core') as c:
    c.attr(label='Virtual Machine Core', style='filled', color='lightblue')
    c.node('interpreter', 'Interpreter')
    c.node('execution_engine', 'Execution Engine')
    c.node('memory', 'Memory Management')
    c.node('instruction_processor', 'Instruction Processor')

with dot.subgraph(name='cluster_bytecode') as c:
    c.attr(label='Bytecode Handling', style='filled', color='lightgreen')
    c.node('codereader', 'CodeReader')
    c.node('codewriter', 'CodeWriter')

with dot.subgraph(name='cluster_ffi') as c:
    c.attr(label='Foreign Function Interface', style='filled', color='lightyellow')
    c.node('ffi_interpreter', 'FFI Interpreter')
    c.node('resurgence_state', 'ResurgenceState')
    c.node('native_functions', 'Native Functions')

with dot.subgraph(name='cluster_objects') as c:
    c.attr(label='Data Structures', style='filled', color='lightpink')
    c.node('instruction', 'Instruction Set')
    c.node('codeholder', 'CodeHolder')
    c.node('constants', 'Constant Pool')

with dot.subgraph(name='cluster_internal') as c:
    c.attr(label='Internal Implementation', style='filled', color='lightgray')
    c.node('imports', 'Imports Manager')
    c.node('instruction_impl', 'Instruction Implementation')

with dot.subgraph(name='cluster_codegen') as c:
    c.attr(label='Code Generation', style='filled', color='lightcyan')
    c.node('codegen', 'Code Generator')

with dot.subgraph(name='cluster_error') as c:
    c.attr(label='Error Handling', style='filled', color='lightcoral')
    c.node('resurgence_error', 'ResurgenceError')
    c.node('error_context', 'Error Context')

dot.edge('codereader', 'codeholder')
dot.edge('codeholder', 'interpreter')
dot.edge('interpreter', 'execution_engine')
dot.edge('execution_engine', 'instruction_processor')
dot.edge('instruction_processor', 'instruction')
dot.edge('instruction', 'instruction_impl')
dot.edge('memory', 'execution_engine')
dot.edge('constants', 'memory')
dot.edge('ffi_interpreter', 'resurgence_state')
dot.edge('resurgence_state', 'native_functions')
dot.edge('imports', 'ffi_interpreter')
dot.edge('codegen', 'codewriter')
dot.edge('resurgence_error', 'error_context')
dot.edge('interpreter', 'resurgence_error', style='dashed')
dot.edge('execution_engine', 'resurgence_error', style='dashed')

dot.edge('external_app', 'ffi_interpreter', label='Embedding')
dot.node('external_app', 'External Application', shape='cylinder')

dot.render('resurgence_vm_architecture', format='png', cleanup=True)