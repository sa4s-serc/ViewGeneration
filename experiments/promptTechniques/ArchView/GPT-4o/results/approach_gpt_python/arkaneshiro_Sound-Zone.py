from graphviz import Digraph

def generate_soundzone_diagram():
    dot = Digraph(comment='Soundzone Web Application Architecture')

    # Nodes
    dot.node('A', 'React Components', shape='rect')
    dot.node('B', 'Redux Store', shape='rect')
    dot.node('C', 'Node.js Server', shape='rect')
    dot.node('D', 'PostgreSQL Database', shape='cylinder')
    dot.node('E', 'Cloudinary Storage', shape='cylinder')

    # Subcomponents of React
    dot.node('A1', 'App.js', shape='rect')
    dot.node('A2', 'Home.js', shape='rect')
    dot.node('A3', 'Profile.js', shape='rect')
    dot.node('A4', 'Dashboard.js', shape='rect')
    dot.node('A5', 'SoundDetail.js', shape='rect')
    dot.node('A6', 'Sound.js', shape='rect')
    dot.node('A7', 'SoundBar.js', shape='rect')
    dot.node('A8', 'Upload.js', shape='rect')
    dot.node('A9', 'LoginForm.js', shape='rect')
    dot.node('A10', 'RegistrationForm.js', shape='rect')
    dot.node('A11', 'NavBar.js', shape='rect')
    dot.node('A12', 'LabelButton.js', shape='rect')

    # Edges
    dot.edge('A', 'B', label='state management', style='dashed')
    dot.edge('B', 'C', label='API calls', style='dashed')
    dot.edge('C', 'D', label='SQL queries', style='solid')
    dot.edge('C', 'E', label='REST API', style='solid')

    # Components within React
    dot.edge('A', 'A1')
    dot.edge('A', 'A2')
    dot.edge('A', 'A3')
    dot.edge('A', 'A4')
    dot.edge('A', 'A5')
    dot.edge('A', 'A6')
    dot.edge('A', 'A7')
    dot.edge('A', 'A8')
    dot.edge('A', 'A9')
    dot.edge('A', 'A10')
    dot.edge('A', 'A11')
    dot.edge('A', 'A12')

    # Draw the diagram
    dot.render('soundzone_diagram', format='png', cleanup=True)

generate_soundzone_diagram()