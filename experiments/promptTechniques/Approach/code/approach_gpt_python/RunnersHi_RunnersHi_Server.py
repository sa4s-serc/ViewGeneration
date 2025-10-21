from graphviz import Digraph

dot = Digraph(comment='RunnersHi Backend Server Architecture')

# Set graph attributes
dot.attr(rankdir='TB', size='10,10')

# Node styles
node_style = {'shape': 'rect', 'style': 'filled', 'fillcolor': 'lightgrey', 'fontname': 'Helvetica'}
controller_style = {'shape': 'rect', 'style': 'filled', 'fillcolor': 'lightblue', 'fontname': 'Helvetica'}
model_style = {'shape': 'rect', 'style': 'filled', 'fillcolor': 'lightgreen', 'fontname': 'Helvetica'}
middleware_style = {'shape': 'rect', 'style': 'filled', 'fillcolor': 'lightyellow', 'fontname': 'Helvetica'}
socket_style = {'shape': 'rect', 'style': 'filled', 'fillcolor': 'lightpink', 'fontname': 'Helvetica'}

# Nodes
dot.node('App', 'app.js', **node_style)
dot.node('AuthMiddleware', 'auth.js', **middleware_style)
dot.node('ErrorHandler', 'ErrorHandler.js', **middleware_style)
dot.node('ResponseHandler', 'responseHandler.js', **middleware_style)

dot.node('UserCtrl', 'userController.js', **controller_style)
dot.node('RankingCtrl', 'rankingController.js', **controller_style)
dot.node('AuthCtrl', 'authController.js', **controller_style)
dot.node('RecordCtrl', 'recordController.js', **controller_style)

dot.node('AuthModel', 'authModel.js', **model_style)
dot.node('UserModel', 'userModel.js', **model_style)
dot.node('RecordModel', 'recordModel.js', **model_style)
dot.node('MatchingModel', 'matchingModel.js', **model_style)
dot.node('RankingModel', 'rankingModel.js', **model_style)

dot.node('Socket', 'socket.js', **socket_style)

# Edges
dot.edge('App', 'AuthMiddleware', label='uses', style='dashed')
dot.edge('App', 'ErrorHandler', label='uses', style='dashed')
dot.edge('App', 'ResponseHandler', label='uses', style='dashed')

dot.edge('App', 'UserCtrl', label='routes')
dot.edge('App', 'RankingCtrl', label='routes')
dot.edge('App', 'AuthCtrl', label='routes')
dot.edge('App', 'RecordCtrl', label='routes')

dot.edge('UserCtrl', 'UserModel', label='interacts')
dot.edge('RankingCtrl', 'RankingModel', label='interacts')
dot.edge('AuthCtrl', 'AuthModel', label='interacts')
dot.edge('RecordCtrl', 'RecordModel', label='interacts')
dot.edge('RecordCtrl', 'MatchingModel', label='interacts')

dot.edge('App', 'Socket', label='real-time', style='dashed')

# Generate the diagram
dot.render('runnershi_backend_architecture', format='png', cleanup=True)