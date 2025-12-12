from graphviz import Digraph

dot = Digraph(comment='JSeat Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue')

# Core components
dot.node('api', 'Java API')
dot.node('cli', 'Command Line\nInterface')
dot.node('processor', 'Seat Allocator\nProcessor')
dot.node('resolver', 'Seat Allocator\nResolver')

# Model components
with dot.subgraph(name='cluster_model') as model:
    model.attr(label='Model Layer')
    model.node('tally', 'Tally')
    model.node('candidate', 'Candidate')
    model.node('result', 'Result')
    model.node('config', 'Processor Config')

# Algorithm components
with dot.subgraph(name='cluster_algorithms') as alg:
    alg.attr(label='Allocation Methods')
    alg.node('majority', 'Majority Based')
    alg.node('largest', 'Largest\nRemainder')
    alg.node('highest', 'Highest\nAverages')
    alg.node('equal', 'Equal\nProportions')

# Customization components
with dot.subgraph(name='cluster_custom') as custom:
    custom.attr(label='Customization')
    custom.node('filters', 'Tally Filters')
    custom.node('decorators', 'Result\nDecorators')
    custom.node('tiebreakers', 'Tie Breakers')

# Define relationships
dot.edge('api', 'processor')
dot.edge('cli', 'processor')
dot.edge('processor', 'resolver')
dot.edge('resolver', 'majority')
dot.edge('resolver', 'largest')
dot.edge('resolver', 'highest')
dot.edge('resolver', 'equal')
dot.edge('processor', 'filters')
dot.edge('processor', 'decorators')
dot.edge('processor', 'tiebreakers')
dot.edge('tally', 'processor')
dot.edge('candidate', 'tally')
dot.edge('processor', 'result')
dot.edge('config', 'processor')

print(dot.source)
dot.render('jseats_architecture', view=True, format='png')