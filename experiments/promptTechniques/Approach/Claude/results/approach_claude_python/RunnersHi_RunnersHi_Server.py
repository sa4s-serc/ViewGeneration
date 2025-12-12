from graphviz import Digraph

# Create a new directed graph
g = Digraph('RunnersHi Backend Architecture')
g.attr(rankdir='TB')

# Define node styles
g.attr('node', shape='rectangle', style='filled', fillcolor='lightblue')

# Add main components
g.node('client', 'Client Apps\n(Mobile)')
g.node('api', 'API Gateway\n(Express.js)')
g.node('socket', 'Socket.IO\n(Real-time Matching)')

# Add middleware layer
with g.subgraph(name='cluster_middleware') as c:
    c.attr(label='Middleware Layer', style='dashed')
    c.node('auth', 'Authentication\n(JWT + bcrypt)')
    c.node('error', 'Error Handler')
    c.node('response', 'Response Formatter')

# Add core services
with g.subgraph(name='cluster_services') as c:
    c.attr(label='Core Services', style='dashed')
    c.node('user_ctrl', 'User Controller')
    c.node('match_ctrl', 'Matching Controller') 
    c.node('record_ctrl', 'Record Controller')
    c.node('rank_ctrl', 'Ranking Controller')

# Add data layer
with g.subgraph(name='cluster_data') as c:
    c.attr(label='Data Layer', style='dashed')
    c.node('user_model', 'User Model')
    c.node('match_model', 'Match Model')
    c.node('record_model', 'Record Model')
    c.node('rank_model', 'Ranking Model')
    c.node('db', 'MySQL Database')

# Add edges
g.edge('client', 'api')
g.edge('client', 'socket')

g.edge('api', 'auth')
g.edge('api', 'error')
g.edge('api', 'response')

g.edge('auth', 'user_ctrl')
g.edge('auth', 'match_ctrl')
g.edge('auth', 'record_ctrl')
g.edge('auth', 'rank_ctrl')

g.edge('socket', 'match_ctrl')

g.edge('user_ctrl', 'user_model')
g.edge('match_ctrl', 'match_model')
g.edge('record_ctrl', 'record_model')
g.edge('rank_ctrl', 'rank_model')

g.edge('user_model', 'db')
g.edge('match_model', 'db')
g.edge('record_model', 'db')
g.edge('rank_model', 'db')

# Save the diagram
g.render('runnershi_architecture', format='png', cleanup=True)