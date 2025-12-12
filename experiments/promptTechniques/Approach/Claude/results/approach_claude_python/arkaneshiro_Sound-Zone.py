from graphviz import Digraph

dot = Digraph(comment='Soundzone Web Application Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded', fontname='Arial')

# Add components
dot.node('client', 'Client Browser')
dot.node('frontend', 'Frontend\n(React/Redux)')
dot.node('auth', 'Authentication\n(JWT)')
dot.node('api', 'Backend API\n(Node.js/Express)')
dot.node('db', 'PostgreSQL\nDatabase')
dot.node('storage', 'Cloudinary\nStorage')

# Add subgraph for frontend components
with dot.subgraph(name='cluster_frontend') as frontend_components:
    frontend_components.attr(label='Frontend Components')
    frontend_components.node('app', 'App.js')
    frontend_components.node('sound', 'Sound.js')
    frontend_components.node('profile', 'Profile.js')
    frontend_components.node('upload', 'Upload.js')
    frontend_components.node('navbar', 'NavBar.js')
    frontend_components.node('soundbar', 'SoundBar.js')

# Add connections
dot.edge('client', 'frontend')
dot.edge('frontend', 'auth')
dot.edge('frontend', 'api')
dot.edge('api', 'db')
dot.edge('api', 'storage')
dot.edge('auth', 'api')

# Add frontend component connections
dot.edge('app', 'sound')
dot.edge('app', 'profile')
dot.edge('app', 'upload')
dot.edge('app', 'navbar')
dot.edge('app', 'soundbar')

# Save the diagram
dot.render('soundzone_architecture', format='png', cleanup=True)