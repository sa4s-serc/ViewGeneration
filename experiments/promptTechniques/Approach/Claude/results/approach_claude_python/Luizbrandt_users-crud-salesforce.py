from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Salesforce User CRUD System Architecture')
dot.attr(rankdir='TB')
dot.attr('node', shape='rectangle', style='rounded,filled', fillcolor='lightgray')

# Create clusters/subgraphs for logical grouping
with dot.subgraph(name='cluster_0') as api_layer:
    api_layer.attr(label='API Layer', style='rounded', color='blue')
    api_layer.node('api_router', 'API Kit Router\n(RAML Spec)')
    api_layer.node('error_handler', 'Error Handler')

with dot.subgraph(name='cluster_1') as impl_layer:
    impl_layer.attr(label='Implementation Layer', style='rounded', color='green') 
    impl_layer.node('mule_flows', 'Mule Flows\n(CRUD Operations)')
    impl_layer.node('dw_transform', 'DataWeave\nTransformations')

with dot.subgraph(name='cluster_2') as security:
    security.attr(label='Security Layer', style='rounded', color='red')
    security.node('secure_props', 'Secure Properties\nModule')
    security.node('secure_config', 'Secure Configuration')

with dot.subgraph(name='cluster_3') as data_layer:
    data_layer.attr(label='Data Layer', style='rounded', color='orange')
    data_layer.node('sf_connector', 'Salesforce\nConnector')
    data_layer.node('sf_db', 'Salesforce\nDatabase')

# Add edges between nodes
dot.edge('api_router', 'mule_flows', 'HTTP Requests')
dot.edge('mule_flows', 'dw_transform', 'Data')
dot.edge('dw_transform', 'sf_connector', 'Transformed Data')
dot.edge('sf_connector', 'sf_db', 'CRUD Operations')
dot.edge('secure_config', 'secure_props', 'Provides')
dot.edge('secure_props', 'sf_connector', 'Credentials')
dot.edge('mule_flows', 'error_handler', 'Exceptions')

# Save the diagram
dot.render('salesforce_architecture', view=True, format='png')