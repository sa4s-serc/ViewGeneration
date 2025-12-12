from graphviz import Digraph

# Create a new directed graph
dot = Digraph(name='koa_architecture', format='png')
dot.attr(rankdir='TB')

# Set global node and edge styles
dot.attr('node', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.attr('edge', fontsize='10')

# Define node clusters for layered architecture
with dot.subgraph(name='cluster_frontend') as frontend:
    frontend.attr(label='Client Layer')
    frontend.node('client', 'Client Applications\n(Browser/API Clients)')

with dot.subgraph(name='cluster_middleware') as middleware:
    middleware.attr(label='Middleware Layer')
    middleware.node('middleware', 'Middleware Stack\n(koa-compose)\n(koa-convert)\n(Session Management)')
    middleware.node('router', 'Router\n(koa-router)')

with dot.subgraph(name='cluster_business') as business:
    business.attr(label='Business Layer')
    business.node('controllers', 'Controllers\n(Request Handling)')
    business.node('services', 'Services\n(Business Logic)')
    business.node('models', 'Models\n(Mongoose Schemas)')

with dot.subgraph(name='cluster_data') as data:
    data.attr(label='Data Layer')
    data.node('mongodb', 'MongoDB\n(Data Storage)')

with dot.subgraph(name='cluster_support') as support:
    support.attr(label='Support Services')
    support.node('testing', 'Testing\n(Ava)')
    support.node('deployment', 'Deployment\n(PM2, Nginx)')
    support.node('monitoring', 'Monitoring\n(Logs, Metrics)')

# Define the relationships
dot.edge('client', 'middleware', 'HTTP Requests')
dot.edge('middleware', 'router', 'Request Pipeline')
dot.edge('router', 'controllers', 'Route Handling')
dot.edge('controllers', 'services', 'Business Operations')
dot.edge('services', 'models', 'Data Operations')
dot.edge('models', 'mongodb', 'CRUD Operations')

# Support service connections
dot.edge('testing', 'controllers', 'Tests', style='dashed')
dot.edge('deployment', 'middleware', 'Deploys', style='dashed')
dot.edge('monitoring', 'middleware', 'Monitors', style='dashed')

# Save the diagram
dot.render('koa_architecture', view=True, cleanup=True)