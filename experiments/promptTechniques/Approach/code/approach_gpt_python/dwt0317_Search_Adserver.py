from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Search Ad Server Architecture', format='png')

# Set graph attributes
dot.attr(rankdir='TB', size='10,8')

# Define colors for different types of components
colors = {
    'Servlets': 'lightblue',
    'Ad Retrieval': 'lightgreen',
    'Advertisement Entity': 'lightyellow',
    'Query Rewriting': 'lightcoral',
    'Elasticsearch Integration': 'lightgrey',
    'Database Interaction': 'lightpink',
    'Configuration': 'lightgoldenrod',
    'Initialization': 'lightcyan',
    'Frontend': 'lightsteelblue'
}

# Add nodes for each component
dot.node('Servlets', 'Servlets', shape='box', style='filled', fillcolor=colors['Servlets'])
dot.node('Ad Retrieval', 'Ad Retrieval', shape='box', style='filled', fillcolor=colors['Ad Retrieval'])
dot.node('Advertisement Entity', 'Advertisement Entity', shape='box', style='filled', fillcolor=colors['Advertisement Entity'])
dot.node('Query Rewriting', 'Query Rewriting', shape='box', style='filled', fillcolor=colors['Query Rewriting'])
dot.node('Elasticsearch Integration', 'Elasticsearch Integration', shape='box', style='filled', fillcolor=colors['Elasticsearch Integration'])
dot.node('Database Interaction', 'Database Interaction', shape='box', style='filled', fillcolor=colors['Database Interaction'])
dot.node('Configuration', 'Configuration', shape='box', style='filled', fillcolor=colors['Configuration'])
dot.node('Initialization', 'Initialization', shape='box', style='filled', fillcolor=colors['Initialization'])
dot.node('Frontend', 'Frontend', shape='box', style='filled', fillcolor=colors['Frontend'])

# Add edges between components
dot.edge('Frontend', 'Servlets', label='HTTP Requests')
dot.edge('Servlets', 'Ad Retrieval', label='Process Requests')
dot.edge('Ad Retrieval', 'Query Rewriting', label='Thrift Call')
dot.edge('Query Rewriting', 'Elasticsearch Integration', label='Retrieve Data')
dot.edge('Ad Retrieval', 'Database Interaction', label='Manage Budgets')
dot.edge('Servlets', 'Configuration', label='Load Config')
dot.edge('Initialization', 'Configuration', label='Initialize')
dot.edge('Servlets', 'Database Interaction', label='Store Logs')
dot.edge('Ad Retrieval', 'Advertisement Entity', label='Use Ad Data')
dot.edge('Ad Retrieval', 'Servlets', label='Return Ads')
dot.edge('Elasticsearch Integration', 'Database Interaction', label='Cache Data')
dot.edge('Initialization', 'Database Interaction', label='Connect to DB')

# Render the graph to a file
dot.render(filename='search_ad_server_architecture')