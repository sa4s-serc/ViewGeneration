from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='NForge DevNote Architecture')

# Define nodes for core components
dot.node('S', 'Server-Side (Node.js/Express)', shape='rectangle')
dot.node('C', 'Client-Side (JavaScript)', shape='rectangle')
dot.node('D', 'Data Storage (Git)', shape='rectangle')
dot.node('F', 'File Attachment', shape='rectangle')
dot.node('U', 'User Management', shape='rectangle')
dot.node('A', 'Admin Tasks', shape='rectangle')
dot.node('R', 'Real-time Collaboration', shape='rectangle')
dot.node('L', 'Localization', shape='rectangle')
dot.node('M', 'Markdown Rendering', shape='rectangle')

# Define nodes for important files
dot.node('app', 'app.coffee', shape='ellipse')
dot.node('config', 'config.js', shape='ellipse')
dot.node('routes', 'routes/index.js', shape='ellipse')
dot.node('gitfs', 'lib/gitfs.js', shape='ellipse')
dot.node('users', 'lib/users.js', shape='ellipse')
dot.node('fileutils', 'lib/fileutils.js', shape='ellipse')
dot.node('graph', 'lib/graph.js', shape='ellipse')
dot.node('renderer', 'lib/renderer.js', shape='ellipse')
dot.node('i18n', 'lib/i18n.js', shape='ellipse')
dot.node('delta', 'lib/delta.js', shape='ellipse')

# Define relationships (edges) between components
dot.edge('S', 'C', label='Express & Socket.IO', arrowhead='normal')
dot.edge('S', 'D', label='Git for Data Storage', arrowhead='normal')
dot.edge('C', 'D', label='AJAX & jQuery', arrowhead='normal')
dot.edge('S', 'F', label='fileApp.coffee', arrowhead='normal')
dot.edge('S', 'U', label='userApp.coffee', arrowhead='normal')
dot.edge('S', 'A', label='adminApp.coffee', arrowhead='normal')
dot.edge('S', 'R', label='Socket.IO', arrowhead='normal')
dot.edge('C', 'L', label='i18n.js & locales', arrowhead='normal')
dot.edge('C', 'M', label='showdown.js & highlight.js', arrowhead='normal')

# Define edges for important files
dot.edge('S', 'app', label='Main Application Setup', arrowhead='normal')
dot.edge('S', 'config', label='Configuration', arrowhead='normal')
dot.edge('S', 'routes', label='Routing', arrowhead='normal')
dot.edge('S', 'gitfs', label='Git Interactions', arrowhead='normal')
dot.edge('S', 'users', label='User Logic', arrowhead='normal')
dot.edge('S', 'fileutils', label='File Operations', arrowhead='normal')
dot.edge('S', 'graph', label='Dependency Resolution', arrowhead='normal')
dot.edge('S', 'renderer', label='Render Operations', arrowhead='normal')
dot.edge('S', 'i18n', label='Internationalization', arrowhead='normal')
dot.edge('S', 'delta', label='Data Patching', arrowhead='normal')

# Render the graph
dot.render('nforge_devnote_architecture', format='png', cleanup=True)