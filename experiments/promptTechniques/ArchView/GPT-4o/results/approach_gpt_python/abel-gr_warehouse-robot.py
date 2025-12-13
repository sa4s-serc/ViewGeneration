from graphviz import Digraph

dot = Digraph(comment='Warehouse Robot Simulation Architecture')

# Set the style for the graph
dot.attr('node', shape='rectangle', style='filled', color='lightgrey')

# Define nodes for each module/component
dot.node('A', 'Unity Environment\n(Visuals)')
dot.node('B', 'CoppeliaSim\n(Physics)')
dot.node('C', 'Python Scripts\n(Logic)')
dot.node('D', 'Web Interface\n(User Interaction)')
dot.node('E', 'Google Cloud Functions\n(Speech-to-Text)')

# Define edges for interactions
dot.edge('A', 'B', label='Client-Server\n(Remote API)', dir='both')
dot.edge('C', 'A', label='Controls Unity')
dot.edge('C', 'B', label='Controls CoppeliaSim')
dot.edge('D', 'A', label='Interacts with\nUnity')
dot.edge('D', 'E', label='Uses\nSpeech-to-Text')
dot.edge('E', 'D', label='Returns\nTranscription')

# Render the graph
dot.render('warehouse_robot_simulation_architecture', format='png', cleanup=True)