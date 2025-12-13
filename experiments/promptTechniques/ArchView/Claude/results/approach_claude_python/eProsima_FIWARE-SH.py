import graphviz

# Create a new directed graph
dot = graphviz.Digraph(comment='FIWARE System Handle Architecture')
dot.attr(rankdir='TB')

# Set global node and edge attributes
dot.attr('node', shape='box', style='rounded', fontname='Arial')
dot.attr('edge', fontname='Arial', fontsize='10')

# Create main system components
dot.node('is', 'Integration Service', shape='component')
dot.node('sh', 'FIWARE System Handle', shape='component')
dot.node('cb', 'FIWARE Context Broker\n(NGSIv2)', shape='cylinder')

# Create core components subgraph
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Core Components', style='rounded', color='gray')
    
    # Core components
    c.node('connector', 'NGSIV2Connector', shape='box')
    c.node('listener', 'Listener\n(ASIO)', shape='box')
    c.node('publisher', 'Publisher', shape='box')
    c.node('subscriber', 'Subscriber', shape='box')
    c.node('conversion', 'Data Conversion\n(xtypes ↔ JSON)', shape='box')

# Add relationships
dot.edge('is', 'sh', 'uses')
dot.edge('sh', 'connector', 'contains')
dot.edge('sh', 'listener', 'contains')
dot.edge('sh', 'publisher', 'contains')
dot.edge('sh', 'subscriber', 'contains')
dot.edge('connector', 'cb', 'NGSIv2 API')
dot.edge('listener', 'connector', 'forwards notifications')
dot.edge('publisher', 'conversion', 'uses')
dot.edge('subscriber', 'conversion', 'uses')
dot.edge('conversion', 'connector', 'translates data')

# Save the diagram
dot.render('fiware_architecture', format='png', cleanup=True)