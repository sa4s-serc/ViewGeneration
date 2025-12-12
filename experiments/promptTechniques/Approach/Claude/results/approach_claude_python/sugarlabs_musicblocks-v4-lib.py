import graphviz

dot = graphviz.Digraph('Architecture View', 
                       comment='Visual Programming Environment Architecture',
                       graph_attr={'rankdir': 'TB'})

# Add nodes/components
dot.node('syntax', 'Syntax Representation\n(Element API, Specification,\nWarehouse, Syntax Tree)', shape='rectangle')
dot.node('execution', 'Execution Engine\n(Symbol Table, Parser,\nInterpreter, Scheduler)', shape='rectangle')
dot.node('library', 'Library\n(Values, Operators,\nConditionals, Loops)', shape='rectangle')

# Add subcomponents
with dot.subgraph(name='cluster_syntax') as c:
    c.attr(label='Syntax Components')
    c.node('element_api', 'Element API')
    c.node('spec', 'Specification')
    c.node('warehouse', 'Warehouse')
    c.node('tree', 'Syntax Tree')
    
with dot.subgraph(name='cluster_execution') as c:
    c.attr(label='Execution Components')
    c.node('symtable', 'Symbol Table')
    c.node('parser', 'Parser')
    c.node('interpreter', 'Interpreter')
    c.node('scheduler', 'Scheduler')

with dot.subgraph(name='cluster_library') as c:
    c.attr(label='Library Elements')
    c.node('values', 'Values')
    c.node('operators', 'Operators')
    c.node('control', 'Control Flow')
    c.node('structures', 'Program Structures')

# Add relationships
dot.edge('syntax', 'execution', 'Provides AST')
dot.edge('library', 'syntax', 'Defines')
dot.edge('execution', 'library', 'Uses')

# Add subcomponent relationships
dot.edge('element_api', 'spec', 'Defines')
dot.edge('spec', 'warehouse', 'Creates')
dot.edge('warehouse', 'tree', 'Builds')
dot.edge('tree', 'parser', 'Parsed by')
dot.edge('parser', 'interpreter', 'Feeds')
dot.edge('interpreter', 'scheduler', 'Schedules')
dot.edge('symtable', 'interpreter', 'References')

print(dot.source)
dot.render('architecture_view', view=True, format='png')