from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='clemgbld_blog_back_office Architecture', format='png')

# Set graph attributes
dot.attr(rankdir='TB', size='10,10')
dot.attr('node', shape='rect', style='filled', color='lightgrey')

# Add nodes for core components
dot.node('Index', 'src/index.tsx\n(Application Entry Point)')
dot.node('App', 'src/App.tsx\n(Routing)')
dot.node('Store', 'src/core/store.ts\n(Redux Store)')
dot.node('Articles', 'src/core/articles\n(Articles Management)')
dot.node('Auth', 'src/core/auth\n(Authentication)')
dot.node('Emails', 'src/core/emails\n(Email Management)')
dot.node('UI', 'src/app/UI\n(UI Components)')
dot.node('Infra', 'src/infrastructure\n(Services)')

# Add nodes for specific functionalities
dot.node('RichTextEditor', 'RichTextEditor\n(Plate)')
dot.node('Redux', 'Redux\n(State Management)')
dot.node('ReactRouter', 'React Router\n(Navigation)')
dot.node('Adapter', 'Adapters\n(Ports & Adapters)')

# Add edges for core application logic
dot.edge('Index', 'App', label='Renders')
dot.edge('App', 'Store', label='Uses')
dot.edge('App', 'Articles', label='Manages')
dot.edge('App', 'Auth', label='Manages')
dot.edge('App', 'Emails', label='Manages')
dot.edge('App', 'UI', label='Uses')
dot.edge('App', 'Infra', label='Interacts')

# Add edges for external libraries and patterns
dot.edge('Articles', 'RichTextEditor', label='Uses')
dot.edge('Store', 'Redux', label='Configured with')
dot.edge('App', 'ReactRouter', label='Configured with')
dot.edge('Infra', 'Adapter', label='Implements')

# Add edges for communication
dot.edge('Index', 'App', label='Initializes', dir='forward')
dot.edge('Infra', 'Store', label='Service Injection', dir='forward')

# Render the graph to a file
dot.render('clemgbld_blog_back_office_architecture', view=True)