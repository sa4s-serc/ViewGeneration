from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='LectureLens Architecture')

# Add nodes for frontend, backend, and database
dot.node('Frontend', 'React Frontend', shape='rectangle', style='filled', color='lightblue')
dot.node('Backend', 'Go Backend', shape='rectangle', style='filled', color='lightcoral')
dot.node('Database', 'PostgreSQL Database', shape='cylinder', style='filled', color='lightgrey')

# Add nodes for key frontend components
dot.node('App', 'App.jsx', shape='rectangle')
dot.node('SyllabusSearch', 'SyllabusSearch.jsx', shape='rectangle')
dot.node('GlassCard', 'GlassCard.jsx', shape='rectangle')
dot.node('LecturePage', 'LecturePage.jsx', shape='rectangle')
dot.node('ReviewItem', 'ReviewItem.jsx', shape='rectangle')
dot.node('Auth', 'Auth.jsx', shape='rectangle')
dot.node('ReviewPost', 'ReviewPost.jsx', shape='rectangle')
dot.node('useQueryReviews', 'useQueryReviews.jsx', shape='rectangle')
dot.node('useMutateReview', 'useMutateReview.jsx', shape='rectangle')
dot.node('store', 'Zustand Store', shape='rectangle')

# Add nodes for key backend components
dot.node('main', 'main.go', shape='rectangle')
dot.node('router', 'router/router.go', shape='rectangle')
dot.node('controller', 'controller/', shape='rectangle')
dot.node('usecase', 'usecase/', shape='rectangle')
dot.node('repository', 'repository/', shape='rectangle')
dot.node('model', 'model/', shape='rectangle')
dot.node('db', 'db/db.go', shape='rectangle')
dot.node('migrate', 'migrate/migrate.go', shape='rectangle')

# Add edges for frontend component interactions
dot.edge('App', 'SyllabusSearch', label='Route')
dot.edge('App', 'LecturePage', label='Route')
dot.edge('LecturePage', 'GlassCard', label='Displays')
dot.edge('LecturePage', 'ReviewItem', label='Displays')
dot.edge('Auth', 'App', label='Integrates')
dot.edge('ReviewPost', 'useMutateReview', label='Uses')
dot.edge('LecturePage', 'useQueryReviews', label='Uses')
dot.edge('store', 'ReviewPost', label='Manages State')

# Add edges for backend component interactions
dot.edge('main', 'router', label='Initializes')
dot.edge('router', 'controller', label='Routes to')
dot.edge('controller', 'usecase', label='Calls')
dot.edge('usecase', 'repository', label='Accesses')
dot.edge('repository', 'model', label='Defines')
dot.edge('main', 'db', label='Connects')
dot.edge('db', 'Database', label='Stores Data')
dot.edge('main', 'migrate', label='Runs')

# Add edges for frontend-backend interactions
dot.edge('Frontend', 'Backend', label='REST API', dir='both')

# Add edge for backend-database interaction
dot.edge('Backend', 'Database', label='Queries', dir='both')

# Render the graph to a file
dot.render('lecturelens_architecture', format='png', cleanup=True)