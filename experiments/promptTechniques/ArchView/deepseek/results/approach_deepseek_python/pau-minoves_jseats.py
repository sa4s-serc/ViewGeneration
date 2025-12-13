import graphviz

dot = graphviz.Digraph(comment='JSeats Architecture')
dot.attr(rankdir='TB', size='8,10')

with dot.subgraph(name='cluster_core') as core:
    core.attr(label='Core Components', style='filled', color='lightgrey')
    core.node('processor', 'SeatAllocatorProcessor', shape='rectangle')
    core.node('config', 'ProcessorConfig', shape='rectangle')
    core.node('resolver', 'SeatAllocatorResolver', shape='rectangle')
    core.node('tally', 'Tally', shape='ellipse')
    core.node('result', 'Result', shape='ellipse')

with dot.subgraph(name='cluster_methods') as methods:
    methods.attr(label='Allocation Methods', style='filled', color='lightblue')
    methods.node('majority', 'Majority Methods', shape='folder')
    methods.node('remainder', 'Largest Remainder', shape='folder')
    methods.node('averages', 'Highest Averages', shape='folder')
    methods.node('proportions', 'Equal Proportions', shape='folder')

with dot.subgraph(name='cluster_plugins') as plugins:
    plugins.attr(label='Plugins', style='filled', color='lightgreen')
    plugins.node('filters', 'Tally Filters', shape='folder')
    plugins.node('decorators', 'Result Decorators', shape='folder')
    plugins.node('tiebreakers', 'Tie Breakers', shape='folder')

dot.edge('config', 'processor', label='configures')
dot.edge('resolver', 'processor', label='resolves')
dot.edge('tally', 'processor', label='input')
dot.edge('processor', 'result', label='output')
dot.edge('processor', 'majority', style='dashed', label='uses')
dot.edge('processor', 'remainder', style='dashed', label='uses')
dot.edge('processor', 'averages', style='dashed', label='uses')
dot.edge('processor', 'proportions', style='dashed', label='uses')
dot.edge('processor', 'filters', style='dashed', label='applies')
dot.edge('processor', 'decorators', style='dashed', label='applies')
dot.edge('processor', 'tiebreakers', style='dashed', label='uses')

dot.render('jseats_architecture', format='png', cleanup=True)