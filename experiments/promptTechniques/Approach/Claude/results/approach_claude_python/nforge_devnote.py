from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='NForge DevNote Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add main components
dot.node('web', 'Web Interface\n(Express/Node.js)')
dot.node('wiki', 'Wiki Module\n(wikiApp.coffee)')
dot.node('user', 'User Management\n(userApp.coffee)')
dot.node('file', 'File Management\n(fileApp.coffee)') 
dot.node('admin', 'Admin Module\n(adminApp.coffee)')
dot.node('git', 'Git Storage\n(gitfs.js)')
dot.node('socket', 'Real-time Updates\n(Socket.IO)')
dot.node('markdown', 'Markdown Processing\n(showdown.js)')

# Add edges
dot.edge('web', 'wiki', 'routes')
dot.edge('web', 'user', 'routes')
dot.edge('web', 'file', 'routes')
dot.edge('web', 'admin', 'routes')
dot.edge('web', 'socket', 'events')

dot.edge('wiki', 'git', 'storage')
dot.edge('file', 'git', 'storage')
dot.edge('wiki', 'markdown', 'render')

dot.edge('socket', 'wiki', 'updates')
dot.edge('user', 'git', 'auth')

# Render the graph
dot.render('nforge_architecture', format='png', cleanup=True)