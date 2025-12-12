import graphviz as gv

dot = gv.Digraph(name='QAPM Architecture', 
                 comment='Android Application Performance Monitoring Library Architecture',
                 format='png')

# Global graph settings
dot.attr(rankdir='TB')
dot.attr('node', shape='rectangle', style='rounded')

# Add main components
dot.node('app', 'Android Application')
dot.node('gradle', 'QAPM Gradle Plugin\n(buildSrc/)')
dot.node('qapm', 'QAPM Library\n(qapm-lib/)')

# Add subcomponents
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Core Monitoring Components')
    c.node('network', 'Network Monitor')
    c.node('fps', 'FPS Monitor')
    c.node('memory', 'Memory Monitor')
    c.node('cpu', 'CPU Monitor')
    c.node('battery', 'Battery Monitor')
    c.node('storage', 'Local Storage')
    c.node('config', 'Config Manager')

# Add relationships
dot.edge('app', 'gradle', 'Build-time injection')
dot.edge('gradle', 'qapm', 'Injects monitoring code')
dot.edge('qapm', 'network')
dot.edge('qapm', 'fps')
dot.edge('qapm', 'memory')
dot.edge('qapm', 'cpu')
dot.edge('qapm', 'battery')
dot.edge('qapm', 'storage')
dot.edge('qapm', 'config')
dot.edge('storage', 'network', 'Report data')

# Generate diagram
dot.render('qapm_architecture', view=True, cleanup=True)