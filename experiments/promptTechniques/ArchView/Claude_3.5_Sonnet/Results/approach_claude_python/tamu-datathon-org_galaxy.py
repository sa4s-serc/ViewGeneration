import graphviz as gv

# Create a new directed graph
dot = gv.Digraph(comment='TAMU Datathon Architecture')
dot.attr(rankdir='TB')

# Add nodes
dot.node('router', 'Router\n(Nginx)', shape='rectangle')
dot.node('gatekeeper', 'Gatekeeper\n(Authentication)', shape='rectangle')
dot.node('obos', 'OBOS\n(Event Management)', shape='rectangle')
dot.node('gigabowser', 'Gigabowser\n(Static Website)', shape='rectangle')
dot.node('user', 'User', shape='oval')
dot.node('domain', 'tamudatathon.com', shape='rectangle')

# Add edges
dot.edge('user', 'domain')
dot.edge('domain', 'router')
dot.edge('router', 'gatekeeper', 'auth requests')
dot.edge('router', 'obos', 'event management')
dot.edge('router', 'gigabowser', 'static content')
dot.edge('gatekeeper', 'obos', 'user data')

# Set graph attributes
dot.attr(fontsize='16')
dot.attr('node', fontsize='12')
dot.attr('edge', fontsize='10')

# Save the diagram
dot.render('tamu_datathon_architecture', format='png', cleanup=True)