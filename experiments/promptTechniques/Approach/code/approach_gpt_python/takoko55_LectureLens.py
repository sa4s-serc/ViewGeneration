from graphviz import Digraph

dot = Digraph(comment='LectureLens Architecture', format='png')

# Frontend Components
dot.node('F', 'Frontend (React)', shape='box', style='filled', fillcolor='lightblue')
dot.node('S', 'SyllabusSearch.jsx', shape='rectangle')
dot.node('G', 'GlassCard.jsx', shape='rectangle')
dot.node('L', 'LecturePage.jsx', shape='rectangle')
dot.node('R', 'ReviewItem.jsx', shape='rectangle')
dot.node('A', 'Auth.jsx', shape='rectangle')
dot.node('RP', 'ReviewPost.jsx', shape='rectangle')
dot.node('UQ', 'useQueryReviews.jsx', shape='rectangle')
dot.node('UM', 'useMutateReview.jsx', shape='rectangle')
dot.node('SI', 'store/index.jsx', shape='rectangle')

# Backend Components
dot.node('B', 'Backend (Go)', shape='box', style='filled', fillcolor='lightyellow')
dot.node('M', 'main.go', shape='rectangle')
dot.node('RO', 'router/router.go', shape='rectangle')
dot.node('C', 'controller/', shape='rectangle', style='dashed')
dot.node('U', 'usecase/', shape='rectangle', style='dashed')
dot.node('RE', 'repository/', shape='rectangle', style='dashed')
dot.node('MO', 'model/', shape='rectangle', style='dashed')
dot.node('DB', 'db/db.go', shape='rectangle')
dot.node('MI', 'migrate/migrate.go', shape='rectangle')

# Database
dot.node('D', 'PostgreSQL Database', shape='cylinder', style='filled', fillcolor='lightgrey')

# Connections - Frontend to Backend
dot.edge('F', 'B', label='RESTful API', dir='both')

# Frontend Internal Connections
dot.edge('F', 'S', label='Uses')
dot.edge('F', 'G', label='Uses')
dot.edge('F', 'L', label='Uses')
dot.edge('F', 'R', label='Uses')
dot.edge('F', 'A', label='Uses')
dot.edge('F', 'RP', label='Uses')
dot.edge('F', 'UQ', label='Uses')
dot.edge('F', 'UM', label='Uses')
dot.edge('F', 'SI', label='Uses')

# Backend Internal Connections
dot.edge('B', 'M', label='Initializes')
dot.edge('B', 'RO', label='Defines Routes')
dot.edge('B', 'C', label='Request Logic')
dot.edge('B', 'U', label='Business Logic')
dot.edge('B', 'RE', label='Data Access')
dot.edge('B', 'MO', label='Data Models')
dot.edge('B', 'DB', label='DB Connection')
dot.edge('B', 'MI', label='DB Migrations')

# Backend to Database
dot.edge('B', 'D', label='GORM')

dot.render('lecturelens_architecture')