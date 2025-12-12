from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Search Ad Server Architecture')
dot.attr(rankdir='TB')

# Add nodes
dot.node('web', 'Web Frontend\n/webapp/search/*', shape='box')
dot.node('servlets', 'Servlets\n(*Servlet.java)', shape='box')
dot.node('adretrieval', 'Ad Retrieval\nAdRetrieval.java', shape='box') 
dot.node('es', 'Elasticsearch\nESHandler.java', shape='box')
dot.node('db', 'MariaDB\nDBPool.java', shape='box')
dot.node('thrift', 'Thrift Services\nRewritingHandler.java', shape='box')
dot.node('logging', 'Logging\nLog4j + Flume', shape='box')

# Add edges with labels
dot.edge('web', 'servlets', 'HTTP')
dot.edge('servlets', 'adretrieval', 'search query')
dot.edge('adretrieval', 'es', 'retrieve ads')
dot.edge('adretrieval', 'db', 'get ad info')
dot.edge('adretrieval', 'thrift', 'rewrite query\nrank ads')
dot.edge('servlets', 'logging', 'log events')
dot.edge('adretrieval', 'logging', 'log impressions')

# Add subgraph for data stores
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Data Stores')
    c.node('es')
    c.node('db')

# Add subgraph for external services  
with dot.subgraph(name='cluster_1') as c:
    c.attr(label='External Services')
    c.node('thrift')
    c.node('logging')

# Save diagram
dot.render('search_ad_server_architecture', format='png', cleanup=True)