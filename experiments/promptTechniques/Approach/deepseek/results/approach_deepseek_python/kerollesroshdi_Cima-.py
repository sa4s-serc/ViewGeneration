import graphviz

dot = graphviz.Digraph(comment='Cima+ iOS Application Architecture')
dot.attr(rankdir='TB', size='8,10')

with dot.subgraph(name='cluster_domain') as c:
    c.attr(label='Domain Layer', style='filled', color='lightgrey')
    c.node('entities', 'Entities\n(Movie, MovieDetails, Genre)', shape='box')
    c.node('repositories', 'Repository Protocols\n(MoviesRepository)', shape='box')
    c.node('usecases', 'Use Cases\n(Browse, Search, MovieDetails)', shape='box')

with dot.subgraph(name='cluster_data') as c:
    c.attr(label='Data Layer', style='filled', color='lightblue')
    c.node('remotedatasource', 'Remote Data Source\n(RemoteMoviesDataSource)', shape='box')
    c.node('repositoryimpl', 'Repository Implementation\n(MoviesRepositoryImpl)', shape='box')
    c.node('moya', 'Moya Service\n(MoviesService)', shape='box')

with dot.subgraph(name='cluster_app') as c:
    c.attr(label='App Layer', style='filled', color='lightgreen')
    c.node('appcoordinator', 'AppCoordinator', shape='box')
    c.node('basevc', 'BaseViewController', shape='box')
    c.node('basevm', 'ViewModel Protocol', shape='box')
    
    with c.subgraph(name='cluster_scenes') as sc:
        sc.attr(label='Scenes', style='filled', color='white')
        sc.node('nowplaying', 'NowPlayingVC\n+ BrowseVM', shape='box')
        sc.node('toprated', 'TopRatedVC\n+ BrowseVM', shape='box')
        sc.node('search', 'SearchVC\n+ SearchVM', shape='box')
        sc.node('moviedetails', 'MovieDetailsVC\n+ MovieDetailsVM', shape='box')
        sc.node('stateview', 'StateView', shape='box')

dot.node('tmdb', 'TMDB API', shape='cylinder', color='orange')
dot.node('rxswift', 'RxSwift\nRxCocoa\nRxMoya', shape='ellipse', color='yellow')

dot.edge('appcoordinator', 'nowplaying', label='navigates to')
dot.edge('appcoordinator', 'toprated', label='navigates to')
dot.edge('appcoordinator', 'search', label='navigates to')
dot.edge('appcoordinator', 'moviedetails', label='navigates to')

dot.edge('nowplaying', 'basevm', style='dashed')
dot.edge('toprated', 'basevm', style='dashed')
dot.edge('search', 'basevm', style='dashed')
dot.edge('moviedetails', 'basevm', style='dashed')

dot.edge('basevc', 'stateview', label='manages')

dot.edge('nowplaying', 'usecases', label='uses', style='dashed')
dot.edge('toprated', 'usecases', label='uses', style='dashed')
dot.edge('search', 'usecases', label='uses', style='dashed')
dot.edge('moviedetails', 'usecases', label='uses', style='dashed')

dot.edge('usecases', 'repositories', label='depends on', style='dashed')
dot.edge('repositoryimpl', 'repositories', label='implements', style='dashed')

dot.edge('repositoryimpl', 'remotedatasource', label='uses')
dot.edge('remotedatasource', 'moya', label='uses')
dot.edge('moya', 'tmdb', label='fetches from')

dot.edge('rxswift', 'nowplaying', style='dashed', color='grey')
dot.edge('rxswift', 'toprated', style='dashed', color='grey')
dot.edge('rxswift', 'search', style='dashed', color='grey')
dot.edge('rxswift', 'moviedetails', style='dashed', color='grey')
dot.edge('rxswift', 'remotedatasource', style='dashed', color='grey')

dot.render('cima_ios_architecture', format='png', cleanup=True)