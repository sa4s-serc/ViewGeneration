import graphviz as gv

# Create a new directed graph
dot = gv.Digraph(comment='Crux Architecture', format='png')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='filled,rounded', fillcolor='lightblue', fontname='Arial')

# Create clusters for different layers
with dot.subgraph(name='cluster_shells') as shells:
    shells.attr(label='Platform-Specific Shells', style='rounded', color='gray')
    shells.node('ios_shell', 'iOS Shell\n(Swift)')
    shells.node('android_shell', 'Android Shell\n(Kotlin)')
    shells.node('web_shell', 'Web Shell\n(TypeScript)')

with dot.subgraph(name='cluster_core') as core:
    core.attr(label='Crux Core', style='rounded', color='darkblue')
    core.node('app_trait', 'App Trait\n(Events, Model, ViewModel)')
    core.node('core_struct', 'Core Struct\n(State Management)')
    core.node('command', 'Command\n(Side Effect Requests)')
    core.node('effect', 'Effect Trait\n(Shell Communication)')

with dot.subgraph(name='cluster_capabilities') as caps:
    caps.attr(label='Capabilities', style='rounded', color='darkgreen')
    caps.node('http_cap', 'HTTP\n(crux_http)')
    caps.node('time_cap', 'Time\n(crux_time)')
    caps.node('storage_cap', 'Storage')

# Bridge component
dot.node('bridge', 'Bridge\n(FFI Boundary)', shape='diamond', style='filled', fillcolor='yellow')

# Testing components
dot.node('testing', 'Testing Support\n(AppTester, Update)', shape='box3d', style='filled', fillcolor='lightgreen')

# Add edges
# Core interactions
dot.edge('app_trait', 'core_struct')
dot.edge('core_struct', 'command')
dot.edge('command', 'effect')
dot.edge('effect', 'bridge')

# Bridge to shells
dot.edge('bridge', 'ios_shell')
dot.edge('bridge', 'android_shell')
dot.edge('bridge', 'web_shell')

# Capabilities
dot.edge('command', 'http_cap')
dot.edge('command', 'time_cap')
dot.edge('command', 'storage_cap')

# Testing
dot.edge('testing', 'app_trait')
dot.edge('testing', 'core_struct')

# Set graph attributes
dot.attr(fontname='Arial')
dot.attr('edge', fontname='Arial', color='gray')

# Save the diagram
dot.render('crux_architecture', view=True, cleanup=True)