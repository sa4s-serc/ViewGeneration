from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Android Application Architecture')

# Define styles for different layers
styles = {
    'graph': {
        'fontsize': '10',
        'fontname': 'Helvetica',
    },
    'nodes': {
        'fontname': 'Helvetica',
        'shape': 'rectangle',
        'style': 'filled',
        'fillcolor': '#ffffff',
    },
    'edges': {
        'style': 'dashed',
        'color': 'black',
    }
}

# Apply styles
dot.attr(**styles['graph'])
dot.node_attr.update(styles['nodes'])
dot.edge_attr.update(styles['edges'])

# Define components
dot.node('MainActivity', 'MainActivity.java\n(View)')
dot.node('MainPresenter', 'MainPresenter.java\n(Presenter)')
dot.node('DataManager', 'DataManager.java\n(Model)')
dot.node('SyncService', 'SyncService.java\n(Service)')
dot.node('DatabaseHelper', 'DatabaseHelper.java\n(SQLite)')
dot.node('RibotsService', 'RibotsService.java\n(Retrofit API)')
dot.node('RibotsAdapter', 'RibotsAdapter.java\n(Adapter)')

# Define data models
dot.node('Ribot', 'Ribot\n(Data Model)')
dot.node('Profile', 'Profile\n(Data Model)')
dot.node('Name', 'Name\n(Data Model)')

# Define testing components
dot.node('UnitTests', 'Unit Tests\n(Mockito, Robolectric, JUnit)')
dot.node('UITests', 'UI Tests\n(Espresso)')

# Define connections (using dashed lines for dependencies)
dot.edge('MainActivity', 'MainPresenter')
dot.edge('MainPresenter', 'DataManager')
dot.edge('DataManager', 'DatabaseHelper')
dot.edge('DataManager', 'RibotsService')
dot.edge('DataManager', 'SyncService')
dot.edge('MainActivity', 'RibotsAdapter')
dot.edge('RibotsAdapter', 'Ribot')
dot.edge('Ribot', 'Profile')
dot.edge('Profile', 'Name')

# Define testing dependencies
dot.edge('UnitTests', 'MainPresenter')
dot.edge('UITests', 'MainActivity')

# Render the diagram
dot.render('android_application_architecture', format='png', cleanup=True)