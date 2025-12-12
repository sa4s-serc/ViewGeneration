import graphviz as gv

# Create a new directed graph
dot = gv.Digraph(comment='Skemi Frontend Architecture')
dot.attr(rankdir='TB')

# Add nodes for main components
dot.node('frontend', 'React Frontend\n(src/App.js)', shape='component')
dot.node('api', 'Rails API\nBackend', shape='component')
dot.node('auth', 'Authentication\n(JWT)', shape='component')
dot.node('state', 'Global State\n(Context + Reducer)', shape='component')
dot.node('services', 'API Services', shape='component')

# Add nodes for key features
dot.node('events', 'Event Management', shape='box')
dot.node('roster', 'Roster Management', shape='box')
dot.node('users', 'User Management', shape='box')
dot.node('ui', 'UI Components\n(Material UI)', shape='box')

# Create subgraph for frontend components
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Frontend Components')
    c.node('nav', 'Navigation')
    c.node('forms', 'Forms')
    c.node('views', 'Views')
    c.node('dialogs', 'Dialogs')

# Add edges to show relationships
dot.edge('frontend', 'state')
dot.edge('frontend', 'auth')
dot.edge('frontend', 'services')
dot.edge('services', 'api')
dot.edge('auth', 'api')
dot.edge('state', 'events')
dot.edge('state', 'roster')
dot.edge('state', 'users')
dot.edge('frontend', 'ui')

# Add edges for frontend components
dot.edge('ui', 'nav')
dot.edge('ui', 'forms')
dot.edge('ui', 'views')
dot.edge('ui', 'dialogs')

# Set graph attributes
dot.attr(fontsize='16')
dot.attr(rankdir='TB')
dot.attr(splines='ortho')

# Save the diagram
dot.render('skemi_frontend_architecture', format='png', cleanup=True)