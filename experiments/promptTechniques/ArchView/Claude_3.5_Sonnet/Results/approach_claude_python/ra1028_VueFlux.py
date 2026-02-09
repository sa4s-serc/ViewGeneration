from graphviz import Digraph

dot = Digraph(comment='VueFlux Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded')

# Add components
dot.node('Store', 'Store\n(Central Hub)')
dot.node('State', 'State\n(Application State)')
dot.node('Actions', 'Actions\n(Intent)')
dot.node('Mutations', 'Mutations\n(State Changes)')
dot.node('Computed', 'Computed\n(Derived State)')
dot.node('UI', 'UI Components')

# VueFluxReactive components
dot.node('Variable', 'Variable\n(Mutable State)')
dot.node('Constant', 'Constant\n(Read-only)')
dot.node('Signal', 'Signal\n(Observable Stream)')
dot.node('Binder', 'Binder\n(UI Binding)')

# Add edges
dot.edge('Actions', 'Store', 'triggers')
dot.edge('Store', 'Mutations', 'dispatches')
dot.edge('Mutations', 'State', 'modifies')
dot.edge('State', 'Computed', 'derives')
dot.edge('Computed', 'UI', 'updates')
dot.edge('Variable', 'Signal', 'emits')
dot.edge('Signal', 'Binder', 'observes')
dot.edge('Binder', 'UI', 'binds')
dot.edge('Constant', 'Signal', 'provides')

# Print the source code
print(dot.source)

# Render the diagram
dot.render('vueflux_architecture', format='png', cleanup=True)