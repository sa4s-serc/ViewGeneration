from graphviz import Digraph

dot = Digraph(comment='Android Application Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='filled', fillcolor='lightgrey')

# Add components
dot.node('UI', 'UI Layer\n(Activities, Fragments, Adapters)')
dot.node('PRES', 'Presentation Layer\n(Presenters)')
dot.node('DATA', 'Data Layer\n(DataManager, Services)')
dot.node('DB', 'Local Storage\n(SQLite, Preferences)')
dot.node('API', 'Remote API\n(Retrofit)')

# Add connections
dot.edge('UI', 'PRES', 'MVP Pattern')
dot.edge('PRES', 'DATA', 'Dependencies')
dot.edge('DATA', 'DB', 'Local Data Access')
dot.edge('DATA', 'API', 'Remote Data Access')

# Print the source code
print(dot.source)

# Render the diagram
dot.render('android_architecture', format='png', cleanup=True)