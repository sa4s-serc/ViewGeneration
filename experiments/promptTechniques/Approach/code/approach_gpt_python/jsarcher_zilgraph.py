from graphviz import Digraph

dot = Digraph(comment='Zilgraph Architecture Overview')

# Set graph attributes
dot.attr(rankdir='LR', size='10,8')

# Components
dot.node('A', 'Zilcrawler\n(Data Acquisition)')
dot.node('B', 'Elasticsearch\n(Data Lake)')
dot.node('C', 'MongoDB\n(Data Warehouse)')
dot.node('D', 'Bokeh Frontend\n(Visualization)')
dot.node('E', 'Nginx\n(Reverse Proxy)')
dot.node('F', 'Zilgraph Oracle\n(Early Stage)')

# Subsystems and interactions
dot.edge('A', 'B', label='Fetch & Store\n(Raw Data)')
dot.edge('B', 'C', label='Aggregate Data')
dot.edge('C', 'D', label='Provide Data for\nVisualization')
dot.edge('D', 'E', label='Served via Reverse Proxy')
dot.edge('F', 'B', label='On-chain Aggregation')

# Add styling for better clarity
dot.attr('node', shape='rectangle', style='filled', color='lightgrey', fontname='Arial')

# Render the graph
dot.format = 'png'
dot.render('zilgraph_architecture', view=True)