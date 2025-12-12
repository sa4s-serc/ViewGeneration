from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Gran Book Application Architecture')

# Define nodes for core components
dot.node('API Gateway', 'API Gateway', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('Auth Service', 'Auth Service', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('User Service', 'User Service', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('Book Service', 'Book Service', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('Review Service', 'Review Service', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('Chat Service', 'Chat Service', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('Admin Panel', 'Admin Panel', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('Database', 'Database', shape='cylinder', style='filled', fillcolor='lightgray')
dot.node('Firebase', 'Firebase', shape='ellipse', style='filled', fillcolor='lightgoldenrod')

# Define edges for communication paths
dot.edge('API Gateway', 'Auth Service', label='REST API', style='dashed')
dot.edge('API Gateway', 'User Service', label='REST API', style='dashed')
dot.edge('API Gateway', 'Book Service', label='REST API', style='dashed')
dot.edge('API Gateway', 'Review Service', label='REST API', style='dashed')
dot.edge('API Gateway', 'Chat Service', label='gRPC', style='dotted')
dot.edge('Admin Panel', 'API Gateway', label='REST API', style='dashed')
dot.edge('Auth Service', 'Firebase', label='Authentication', style='dashed')
dot.edge('User Service', 'Database', label='CRUD Operations', style='dashed')
dot.edge('Book Service', 'Database', label='CRUD Operations', style='dashed')
dot.edge('Review Service', 'Database', label='CRUD Operations', style='dashed')
dot.edge('Chat Service', 'Database', label='CRUD Operations', style='dashed')

# Render the graph
dot.render('gran_book_architecture', format='png', cleanup=True)