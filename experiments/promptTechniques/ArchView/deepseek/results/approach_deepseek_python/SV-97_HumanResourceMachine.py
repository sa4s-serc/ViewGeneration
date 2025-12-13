import graphviz

dot = graphviz.Digraph(comment='HRM Virtual Machine Architecture')
dot.attr(rankdir='TB', size='8,10')

# Main components
with dot.subgraph(name='cluster_compiler') as c:
    c.attr(label='Compiler', style='filled', color='lightgrey')
    c.node('tokenizer', 'Tokenizer\n(Python/Rust)', shape='box', style='filled', color='lightblue')
    c.node('translator', 'Translator/Assembler\n(Python/Rust)', shape='box', style='filled', color='lightblue')
    c.node('disassembler', 'Bytecode Disassembler\n(Python/Rust)', shape='box', style='filled', color='lightblue')

with dot.subgraph(name='cluster_vm') as v:
    v.attr(label='Virtual Machine', style='filled', color='lightyellow')
    v.node('vm', 'VM Core\n(Python/Rust)', shape='box', style='filled', color='orange')
    v.node('logger', 'Logger\n(Rust)', shape='box', style='filled', color='orange')

# Input/Output components
dot.node('input', 'HRM Assembly\nInput', shape='ellipse', style='filled', color='lightgreen')
dot.node('bytecode', 'Bytecode\nOutput', shape='ellipse', style='filled', color='lightcoral')
dot.node('execution', 'Program\nExecution', shape='ellipse', style='filled', color='lightcoral')

# Connections
dot.edge('input', 'tokenizer', label='parse')
dot.edge('tokenizer', 'translator', label='tokens')
dot.edge('translator', 'bytecode', label='generate')
dot.edge('bytecode', 'vm', label='execute')
dot.edge('vm', 'execution', label='run')
dot.edge('translator', 'disassembler', label='translate', style='dashed')
dot.edge('disassembler', 'bytecode', label='disassemble', style='dashed')
dot.edge('vm', 'logger', label='log', style='dotted')

# Design patterns annotation
dot.node('patterns', 'Design Patterns:\n- State Machine (Tokenizer)\n- Command Pattern (VM)\n- Iterator Pattern', shape='note', style='filled', color='wheat')

dot.render('hrm_architecture', format='png', cleanup=True)