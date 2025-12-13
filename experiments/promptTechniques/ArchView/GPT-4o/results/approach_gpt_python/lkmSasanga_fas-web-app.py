from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='fas-web-app Architecture')

# Define nodes for major components
dot.node('UI', 'UI Components', shape='rect', style='filled', color='lightblue')
dot.node('Auth', 'User Authentication', shape='rect', style='filled', color='lightgreen')
dot.node('Search', 'Search and Analysis', shape='rect', style='filled', color='lightyellow')
dot.node('Dashboard', 'Dashboard', shape='rect', style='filled', color='lightcoral')
dot.node('DataVis', 'Data Visualization', shape='rect', style='filled', color='lightsalmon')
dot.node('Reusable', 'Reusable UI Components', shape='rect', style='filled', color='lightgrey')
dot.node('BackendAPI', 'Backend API', shape='rect', style='filled', color='lightcyan')
dot.node('Firebase', 'Firebase Hosting', shape='rect', style='filled', color='wheat')

# Define edges for interactions
dot.edge('UI', 'Auth', label='User Login/Signup', arrowhead='normal')
dot.edge('UI', 'Search', label='Item Search', arrowhead='normal')
dot.edge('UI', 'Dashboard', label='View Analysis Results', arrowhead='normal')
dot.edge('UI', 'DataVis', label='Visualize Data', arrowhead='normal')
dot.edge('Dashboard', 'DataVis', label='Fetch Data', arrowhead='normal')
dot.edge('DataVis', 'BackendAPI', label='Get Sentiment Data', arrowhead='normal')
dot.edge('Search', 'BackendAPI', label='Query Sentiments', arrowhead='normal')
dot.edge('Reusable', 'UI', label='Use Components', arrowhead='normal')
dot.edge('UI', 'Firebase', label='Deployment', arrowhead='normal')

# View the diagram
dot.render('fas-web-app-architecture', format='png', cleanup=True)