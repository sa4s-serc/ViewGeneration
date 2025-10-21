from graphviz import Digraph

# Create a Digraph object
dot = Digraph(comment='Pokemon Game Architecture')

# Define nodes for key components
dot.node('CS', 'Client-Server Architecture', shape='rect', style='filled', fillcolor='lightblue')
dot.node('GUI', 'GUI-Driven Client (Qt)', shape='rect', style='filled', fillcolor='lightgreen')
dot.node('DB', 'Data Persistence (SQLite)', shape='rect', style='filled', fillcolor='lightyellow')
dot.node('JSON', 'JSON Communication', shape='rect', style='filled', fillcolor='lightcoral')
dot.node('TF', 'Testing Framework (Catch2)', shape='rect', style='filled', fillcolor='lightgrey')

# Define nodes for additional components
dot.node('Project', 'Project Definition', shape='rect')
dot.node('Comm', 'Communication (Sockets)', shape='rect')
dot.node('DataMng', 'Data Management (ORM)', shape='rect')
dot.node('GameLogic', 'Game Logic', shape='rect')
dot.node('GUIComponents', 'GUI Components', shape='rect')
dot.node('ReqHandling', 'Server Request Handling', shape='rect')

# Define edges to represent dependencies
dot.edge('CS', 'GUI', label='integrates with', dir='forward')
dot.edge('CS', 'DB', label='stores data in', dir='forward')
dot.edge('CS', 'JSON', label='uses for communication', dir='forward')
dot.edge('CS', 'TF', label='tested by', dir='forward')
dot.edge('GUI', 'GUIComponents', label='includes', dir='forward')
dot.edge('DB', 'DataMng', label='managed by', dir='forward')
dot.edge('Comm', 'Project', label='defined in', dir='forward')
dot.edge('GameLogic', 'ReqHandling', label='executes', dir='forward')

# Render the diagram
dot.render('pokemon_game_architecture', format='png', cleanup=True)