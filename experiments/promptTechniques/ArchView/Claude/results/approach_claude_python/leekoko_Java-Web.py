from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Multi-Tier Architecture')
dot.attr(rankdir='TB')

# Add nodes
dot.node('web', 'Frontend\n(HTML/CSS/jQuery)', shape='box')
dot.node('app', 'Application Layer\n(Java Servlets/Spring Boot)', shape='box') 
dot.node('cache', 'Redis Cache', shape='cylinder')
dot.node('db', 'MySQL Database', shape='cylinder')
dot.node('dubbo', 'Dubbo Service Registry', shape='box')
dot.node('tomcat', 'Tomcat Server', shape='box')
dot.node('security', 'Security Layer\n(Shiro/OAuth2)', shape='box')

# Add edges
dot.edge('web', 'app', 'HTTP/AJAX')
dot.edge('app', 'cache', 'Cache Operations')
dot.edge('app', 'db', 'JDBC')
dot.edge('app', 'dubbo', 'Service Discovery')
dot.edge('app', 'security', 'Auth')
dot.edge('tomcat', 'app', 'Hosts')

# Add subgraphs for logical grouping
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Data Layer')
    c.node('cache')
    c.node('db')

with dot.subgraph(name='cluster_1') as c:
    c.attr(label='Service Layer') 
    c.node('app')
    c.node('dubbo')
    c.node('security')

# Set graph attributes
dot.attr(fontsize='16')
dot.attr(rankdir='TB')

# Save the diagram
dot.render('architecture_diagram', format='png', cleanup=True)