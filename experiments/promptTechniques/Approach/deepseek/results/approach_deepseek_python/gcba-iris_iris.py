import graphviz

dot = graphviz.Digraph(comment='Iris IoT Backend Framework Architecture')
dot.attr(rankdir='TB', size='8,10', concentrate='true')

# Core Components
dot.node('Dock', 'Dock\n(Listens for messages,\nparses, sends to Dispatcher)', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('Dispatcher', 'Dispatcher\n(Routes messages,\nmanages data flow)', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('Handler', 'Handler\n(Processes data,\ngenerates response)', shape='rectangle', style='filled', fillcolor='lightyellow')
dot.node('Hook', 'Hook\n(Executes custom logic\non data)', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('Flow', 'Flow\n(Defines message path)', shape='rectangle', style='filled', fillcolor='lightgray')
dot.node('ThreadPool', 'Thread Pool\n(Concurrent processing)', shape='rectangle', style='filled', fillcolor='plum')
dot.node('CLI', 'CLI Tool\n(Project management,\nflow execution)', shape='rectangle', style='filled', fillcolor='wheat')
dot.node('Logger', 'Logger\n(Winston logging)', shape='rectangle', style='filled', fillcolor='silver')
dot.node('Validator', 'Validator\n(Configuration validation)', shape='rectangle', style='filled', fillcolor='tan')

# External/Supporting Components
dot.node('Config', 'Configuration\n(Application settings)', shape='ellipse', style='filled', fillcolor='bisque')
dot.node('Events', 'Event System\n(Observer pattern)', shape='ellipse', style='filled', fillcolor='lightcyan')

# Data Flow Connections
dot.edge('Dock', 'Dispatcher', label='parsed messages', color='blue')
dot.edge('Dispatcher', 'Handler', label='data objects', color='blue')
dot.edge('Dispatcher', 'Hook', label='data for processing', color='blue', dir='both')
dot.edge('Flow', 'Dispatcher', label='flow definition', color='green')
dot.edge('Dispatcher', 'ThreadPool', label='jobs for execution', color='purple')
dot.edge('ThreadPool', 'Dispatcher', label='processed results', color='purple')

# Management and Support Connections
dot.edge('CLI', 'Flow', label='flow management', color='orange')
dot.edge('CLI', 'Dispatcher', label='execution commands', color='orange')
dot.edge('Config', 'Dock', label='configuration', color='red', style='dashed')
dot.edge('Config', 'Dispatcher', label='configuration', color='red', style='dashed')
dot.edge('Config', 'Handler', label='configuration', color='red', style='dashed')
dot.edge('Config', 'Hook', label='configuration', color='red', style='dashed')
dot.edge('Events', 'Dock', label='event notifications', color='cyan', style='dashed')
dot.edge('Events', 'Dispatcher', label='event notifications', color='cyan', style='dashed')
dot.edge('Events', 'Handler', label='event notifications', color='cyan', style='dashed')
dot.edge('Logger', 'Dock', label='logging', color='gray', style='dashed')
dot.edge('Logger', 'Dispatcher', label='logging', color='gray', style='dashed')
dot.edge('Logger', 'Handler', label='logging', color='gray', style='dashed')
dot.edge('Validator', 'Config', label='validation', color='brown', style='dashed')

# Plugin Architecture Group
with dot.subgraph(name='cluster_plugins') as c:
    c.attr(label='Plugin System', style='dashed', color='purple')
    c.node('DockPlugin', 'Dock Plugins\n(Hot Reload)', shape='rectangle', style='filled', fillcolor='lightblue')
    c.node('HandlerPlugin', 'Handler Plugins', shape='rectangle', style='filled', fillcolor='lightyellow')
    c.node('HookPlugin', 'Hook Plugins', shape='rectangle', style='filled', fillcolor='lightcoral')
    c.edge('DockPlugin', 'Dispatcher', label='parsed messages', color='blue')
    c.edge('Dispatcher', 'HandlerPlugin', label='data objects', color='blue')
    c.edge('Dispatcher', 'HookPlugin', label='data for processing', color='blue', dir='both')

dot.render('iris_architecture', format='png', cleanup=True)