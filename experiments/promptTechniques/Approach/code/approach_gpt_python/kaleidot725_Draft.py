from graphviz import Digraph

# Create a Digraph object
dot = Digraph(comment='Emomemo App Architecture')

# Set graph attributes
dot.attr(rankdir='TB', size='10,8')
dot.attr('node', shape='rect', style='filled', color='lightgrey')

# Add nodes for each module
dot.node('App', 'App Module')
dot.node('Domain', 'Domain Module')
dot.node('Data', 'Data Module')

# Add nodes for key components in the app module
dot.node('ComposeUI', 'Jetpack Compose UI')
dot.node('NavCompose', 'Navigation Compose')
dot.node('TextEditor', 'Custom TextEditor')
dot.node('MainActivity', 'ComposeMainActivity')
dot.node('EmomemoApp', 'EmomemoApp.kt')

# Add nodes for key components in the data module
dot.node('RoomDB', 'Room Database')
dot.node('Repositories', 'Repositories')

# Add nodes for key components in the domain module
dot.node('UseCases', 'Use Cases')

# Add nodes for technology stack
dot.node('Koin', 'Koin')
dot.node('Coroutines', 'Kotlin Coroutines and Flows')
dot.node('JUnit', 'JUnit')

# Add edges for the app module
dot.edge('App', 'ComposeUI')
dot.edge('App', 'NavCompose')
dot.edge('App', 'TextEditor')
dot.edge('App', 'MainActivity')
dot.edge('App', 'EmomemoApp')

# Add edges for the data module
dot.edge('Data', 'RoomDB')
dot.edge('Data', 'Repositories')

# Add edges for the domain module
dot.edge('Domain', 'UseCases')

# Add connections between modules
dot.edge('MainActivity', 'ComposeUI', label='hosts')
dot.edge('ComposeUI', 'NavCompose', label='manages')
dot.edge('TextEditor', 'ComposeUI', label='integrates')
dot.edge('EmomemoApp', 'Koin', label='initializes')
dot.edge('Repositories', 'RoomDB', label='accesses')
dot.edge('UseCases', 'Repositories', label='orchestrates')
dot.edge('UseCases', 'Coroutines', label='uses')
dot.edge('App', 'JUnit', label='tests')

# Add technology stack connections
dot.edge('EmomemoApp', 'Koin', label='DI')
dot.edge('Domain', 'Coroutines', label='Async Processing')

# Render the graph
dot.render('emomemo_architecture', format='png', cleanup=True)