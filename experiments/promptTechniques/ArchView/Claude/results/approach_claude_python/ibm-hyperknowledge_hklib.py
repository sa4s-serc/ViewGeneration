from graphviz import Digraph

dot = Digraph(comment='HKLib Architecture View')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded')

# Core Layer
with dot.subgraph(name='cluster_0') as core:
    core.attr(label='Core Entity Layer')
    core.attr('node', color='lightblue', style='filled')
    core.node('HKEntity', 'HKEntity\n(Abstract Base)')
    core.node('Node', 'Node')
    core.node('Context', 'Context')
    core.node('Link', 'Link')
    core.node('Connector', 'Connector')
    core.node('Reference', 'Reference')
    core.node('Trail', 'Trail')
    core.node('Virtual', 'Virtual Entities')

    # Core relationships
    core.edge('HKEntity', 'Node')
    core.edge('HKEntity', 'Context')
    core.edge('HKEntity', 'Link')
    core.edge('HKEntity', 'Connector')
    core.edge('HKEntity', 'Reference')
    core.edge('HKEntity', 'Trail')
    core.edge('HKEntity', 'Virtual')

# Data Access Layer
with dot.subgraph(name='cluster_1') as dal:
    dal.attr(label='Data Access Layer')
    dal.attr('node', color='lightgreen', style='filled')
    dal.node('HKDatasource', 'HKDatasource\n(DAO)')
    dal.node('Observer', 'Observer Pattern')
    dal.node('Serialization', 'Serialization')

# Utility Layer
with dot.subgraph(name='cluster_2') as util:
    util.attr(label='Utility Layer')
    util.attr('node', color='lightyellow', style='filled')
    util.node('GraphBuilder', 'Graph Builder')
    util.node('FI', 'Fragment Identifiers')
    util.node('ExternalData', 'External Data\nIntegration')

# Cross-layer relationships
dot.edge('HKDatasource', 'HKEntity')
dot.edge('Observer', 'HKDatasource')
dot.edge('GraphBuilder', 'HKEntity')
dot.edge('Serialization', 'HKEntity')
dot.edge('FI', 'Node')
dot.edge('ExternalData', 'Virtual')

# Print the DOT source
print(dot.source)

# Render the diagram
dot.render('hklib_architecture', view=True, format='png')