from graphviz import Digraph

dot = Digraph(comment='HRM Virtual Machine Architecture')

# Define nodes for components
dot.node('T', 'Tokenizer')
dot.node('TA', 'Translator/Assembler')
dot.node('BD', 'Bytecode Disassembler')
dot.node('VM', 'Virtual Machine')
dot.node('L', 'Logger')

# Define nodes for files
dot.node('FT', 'fancy_translator.py')
dot.node('TV', 'translator.py')
dot.node('PV', 'prototype/vm.py')
dot.node('BS', 'bubble_sort.hrm')
dot.node('ST', 'simple_test.hrm')
dot.node('OH', 'out.hrm')
dot.node('OC', 'out.hrmc')

# Define edges for control flow and interactions
dot.edge('T', 'TA', label='tokenizes')
dot.edge('TA', 'VM', label='translates to bytecode')
dot.edge('VM', 'BD', label='executes and disassembles')
dot.edge('L', 'VM', label='logs execution')
dot.edge('FT', 'T', label='implements')
dot.edge('TV', 'TA', label='implements')
dot.edge('PV', 'VM', label='implements')
dot.edge('BS', 'FT', label='example code')
dot.edge('ST', 'FT', label='example code')
dot.edge('OH', 'BD', label='assembly output')
dot.edge('OC', 'BD', label='bytecode output')

# Render the graph
dot.render('hrm_virtual_machine_architecture', format='png', cleanup=True)