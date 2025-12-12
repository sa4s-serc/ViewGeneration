import graphviz

dot = graphviz.Digraph('Architecture View', 
                      comment='Emomemo Architecture View',
                      graph_attr={'rankdir': 'TB'})

# Add nodes for layers
dot.node('presentation', 'Presentation Layer\n(Jetpack Compose UI)', shape='box', style='filled', fillcolor='lightblue')
dot.node('domain', 'Domain Layer\n(Use Cases)', shape='box', style='filled', fillcolor='lightgreen')
dot.node('data', 'Data Layer\n(Repositories)', shape='box', style='filled', fillcolor='lightyellow')
dot.node('db', 'Local Storage\n(Room Database)', shape='cylinder', style='filled', fillcolor='lightgray')

# Add nodes for key components
dot.node('main_activity', 'ComposeMainActivity', shape='component')
dot.node('viewmodels', 'ViewModels\n(MVI Pattern)', shape='component') 
dot.node('usecases', 'Use Cases\n(Business Logic)', shape='component')
dot.node('repositories', 'Repositories', shape='component')
dot.node('dao', 'DAOs', shape='component')

# Add edges to show relationships
dot.edge('main_activity', 'viewmodels', 'observes')
dot.edge('viewmodels', 'usecases', 'calls')
dot.edge('usecases', 'repositories', 'uses')
dot.edge('repositories', 'dao', 'uses')
dot.edge('dao', 'db', 'accesses')

# Add containment relationships
with dot.subgraph(name='cluster_presentation') as p:
    p.attr(label='', style='dashed')
    p.node('main_activity')
    p.node('viewmodels')
dot.edge('presentation', 'cluster_presentation', style='invisible')

with dot.subgraph(name='cluster_domain') as d:
    d.attr(label='', style='dashed')
    d.node('usecases')
dot.edge('domain', 'cluster_domain', style='invisible')

with dot.subgraph(name='cluster_data') as da:
    da.attr(label='', style='dashed')
    da.node('repositories')
    da.node('dao')
    da.node('db')
dot.edge('data', 'cluster_data', style='invisible')

dot.render('architecture_view', view=True, format='png')