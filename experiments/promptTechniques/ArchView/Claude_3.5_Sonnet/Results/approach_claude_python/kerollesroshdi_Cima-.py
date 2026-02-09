from graphviz import Digraph

dot = Digraph(comment='MVVM Clean Architecture - Cima+ iOS App')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Create main layers
with dot.subgraph(name='cluster_0') as presentation:
    presentation.attr(label='Presentation Layer')
    presentation.attr('node', fillcolor='lightblue', style='filled,rounded')
    presentation.node('views', 'Views\n(UIViewControllers)')
    presentation.node('viewmodels', 'ViewModels')
    presentation.node('coordinator', 'AppCoordinator')

with dot.subgraph(name='cluster_1') as domain:
    domain.attr(label='Domain Layer')
    domain.attr('node', fillcolor='lightgreen', style='filled,rounded')
    domain.node('usecases', 'Use Cases')
    domain.node('entities', 'Entities')
    domain.node('repositories', 'Repository\nInterfaces')

with dot.subgraph(name='cluster_2') as data:
    data.attr(label='Data Layer')
    data.attr('node', fillcolor='lightyellow', style='filled,rounded')
    data.node('repository_impl', 'Repository\nImplementations')
    data.node('remote_data', 'Remote Data\nSources')
    data.node('api', 'TMDB API')

# Define relationships
dot.edge('views', 'viewmodels', 'observes')
dot.edge('viewmodels', 'usecases', 'uses')
dot.edge('usecases', 'repositories', 'uses')
dot.edge('repositories', 'entities', 'uses')
dot.edge('repository_impl', 'repositories', 'implements')
dot.edge('repository_impl', 'remote_data', 'uses')
dot.edge('remote_data', 'api', 'calls')
dot.edge('coordinator', 'views', 'manages')

# Save the diagram
dot.render('cima_architecture', format='png', cleanup=True)