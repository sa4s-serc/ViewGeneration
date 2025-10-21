from graphviz import Digraph

dot = Digraph(comment='VueFlux Architecture')

# Nodes
dot.node('A', 'Actions', shape='rect')
dot.node('M', 'Mutations', shape='rect')
dot.node('S', 'State', shape='rect')
dot.node('C', 'Computed', shape='rect')
dot.node('St', 'Store', shape='rect', style='filled', fillcolor='lightgrey')
dot.node('V', 'Variable', shape='rect')
dot.node('Co', 'Constant', shape='rect')
dot.node('Si', 'Sink', shape='rect')
dot.node('Sig', 'Signal', shape='rect')
dot.node('B', 'Binder', shape='rect')
dot.node('Ex', 'Executor', shape='rect')
dot.node('AR', 'AtomicReference', shape='rect')

# Edges
dot.edge('A', 'M', label='triggers', arrowhead='normal')
dot.edge('M', 'S', label='modifies', arrowhead='normal')
dot.edge('S', 'C', label='provides', arrowhead='normal')
dot.edge('C', 'St', label='observed by UI', arrowhead='normal')
dot.edge('V', 'Sig', label='emits signals', arrowhead='normal')
dot.edge('Si', 'Sig', label='produces signals', arrowhead='normal')
dot.edge('Sig', 'B', label='binds to UI', arrowhead='normal')
dot.edge('Ex', 'A', label='controls execution', arrowhead='normal')
dot.edge('AR', 'S', label='ensures thread safety', arrowhead='normal')

dot.render('vueflux_architecture', format='png', cleanup=True)