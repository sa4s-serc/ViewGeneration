from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='hklib Architecture')

# Define styles for different components
styles = {
    'entity': {'shape': 'rect', 'style': 'filled', 'fillcolor': 'lightblue'},
    'datasource': {'shape': 'rect', 'style': 'filled', 'fillcolor': 'lightgreen'},
    'utility': {'shape': 'rect', 'style': 'filled', 'fillcolor': 'lightcoral'},
    'observer': {'shape': 'rect', 'style': 'filled', 'fillcolor': 'lightgoldenrod'}
}

# Add nodes for core entity components
dot.node('Node', 'Node', **styles['entity'])
dot.node('Context', 'Context', **styles['entity'])
dot.node('Link', 'Link', **styles['entity'])
dot.node('Connector', 'Connector', **styles['entity'])
dot.node('Reference', 'Reference', **styles['entity'])
dot.node('Trail', 'Trail', **styles['entity'])
dot.node('HKEntity', 'HKEntity', **styles['entity'])

# Add nodes for HKDatasource
dot.node('HKDatasource', 'HKDatasource', **styles['datasource'])
dot.node('Query', 'Query', **styles['datasource'])

# Add nodes for Fragment Identifiers
dot.node('FI', 'FI', **styles['utility'])
dot.node('FIAnchor', 'FIAnchor', **styles['utility'])
dot.node('FIOperator', 'FIOperator', **styles['utility'])

# Add nodes for Observer Pattern
dot.node('HKObserverFactory', 'HKObserverFactory', **styles['observer'])
dot.node('ObserverClient', 'ObserverClient', **styles['observer'])

# Add nodes for External Data Integration
dot.node('ExternalData', 'External Data', **styles['utility'])

# Add edges to show relationships
dot.edge('HKEntity', 'Node')
dot.edge('HKEntity', 'Context')
dot.edge('HKEntity', 'Link')
dot.edge('HKEntity', 'Connector')
dot.edge('HKEntity', 'Reference')
dot.edge('HKEntity', 'Trail')

dot.edge('HKDatasource', 'Query', label='uses')
dot.edge('HKObserverFactory', 'ObserverClient', label='creates')

dot.edge('Node', 'ExternalData', label='interacts')
dot.edge('Context', 'ExternalData', label='interacts')
dot.edge('Link', 'ExternalData', label='interacts')

dot.edge('FI', 'FIAnchor', label='contains')
dot.edge('FI', 'FIOperator', label='contains')

# Render the graph to a file
dot.render('hklib_architecture', format='png', cleanup=True)