import graphviz

dot = graphviz.Digraph('HRM_Architecture', 
                       comment='HRM Virtual Machine Architecture',
                       graph_attr={'rankdir': 'LR'})

# Add nodes
dot.node('assembly', 'HRM Assembly\nCode', shape='note')
dot.node('tokenizer', 'Tokenizer', shape='component')
dot.node('translator', 'Translator/\nAssembler', shape='component')
dot.node('bytecode', 'Bytecode', shape='note')
dot.node('vm', 'Virtual Machine', shape='component')
dot.node('disassembler', 'Bytecode\nDisassembler', shape='component')
dot.node('logger', 'Logger', shape='component')

# Add subgraph for compiler components
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Compiler Pipeline')
    c.attr('node', shape='component')
    c.edge('tokenizer', 'translator')

# Add edges
dot.edge('assembly', 'tokenizer', 'input')
dot.edge('translator', 'bytecode', 'generates')
dot.edge('bytecode', 'vm', 'executes')
dot.edge('bytecode', 'disassembler', 'input')
dot.edge('disassembler', 'assembly', 'generates', constraint='false')
dot.edge('vm', 'logger', 'logs')

# Set graph attributes
dot.attr(rankdir='LR')
dot.attr(splines='ortho')

# Render the graph
dot.render('hrm_architecture', view=True, format='png')