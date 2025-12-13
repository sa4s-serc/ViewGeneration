import graphviz as gv

# Create a new directed graph
dot = gv.Digraph(comment='Zilgraph Architecture View')
dot.attr(rankdir='TB')

# Add nodes for main components
dot.node('crawler', 'Zilcrawler\n(Data Acquisition)', shape='box')
dot.node('elastic', 'Elasticsearch\n(Raw Data Storage)', shape='cylinder')
dot.node('mongodb', 'MongoDB\n(Aggregated Data)', shape='cylinder')
dot.node('frontend', 'Frontend\n(Bokeh + Kibana)', shape='box')
dot.node('zilswap', 'Zilswap Interface', shape='box')
dot.node('oracle', 'Zilgraph Oracle\n(Early Stage)', shape='box', style='dashed')

# Add edges to show relationships and data flow
dot.edge('crawler', 'elastic', 'Raw Transaction Data')
dot.edge('elastic', 'mongodb', 'Aggregated Data')
dot.edge('mongodb', 'frontend', 'Dashboard Data')
dot.edge('zilswap', 'crawler', 'Blockchain Data')
dot.edge('mongodb', 'oracle', 'Aggregated Data', style='dashed')
dot.edge('oracle', 'zilswap', 'On-chain Data Feed', style='dashed')

# Add subgraph for data storage
with dot.subgraph(name='cluster_storage') as s:
    s.attr(label='Data Storage Layer')
    s.node('elastic')
    s.node('mongodb')

# Add subgraph for presentation layer
with dot.subgraph(name='cluster_presentation') as p:
    p.attr(label='Presentation Layer')
    p.node('frontend')

# Print the source code
print(dot.source)

# Render the diagram
dot.render('zilgraph_architecture', format='png', cleanup=True)