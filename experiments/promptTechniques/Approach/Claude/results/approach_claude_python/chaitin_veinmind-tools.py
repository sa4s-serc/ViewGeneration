from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Veinmind-Tools Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightgray')
dot.attr('edge', fontsize='10')

# Create clusters/subgraphs
with dot.subgraph(name='cluster_core') as core:
    core.attr(label='Core Components', style='rounded', bgcolor='lightblue')
    core.node('runner', 'Veinmind Runner\nService Management\nPlugin Orchestration', shape='component')
    core.node('libvein', 'libveinmind\nContainer Runtime Interface', shape='component')
    core.node('config', 'TOML Configuration\nService Definition', shape='note')

with dot.subgraph(name='cluster_plugins') as plugins:
    plugins.attr(label='Security Plugins', style='rounded', bgcolor='lightgreen')
    plugins.node('malware', 'Malware Detection')
    plugins.node('weakpass', 'Password Analysis\n(Tomcat/Redis/SSH/MySQL)', shape='box')
    plugins.node('mount', 'Mount Point Security')
    plugins.node('sensitive', 'Sensitive Data Scanner')
    plugins.node('cve', 'CVE Detection')
    plugins.node('intrusion', 'Intrusion Detection')

with dot.subgraph(name='cluster_output') as output:
    output.attr(label='Output & Storage', style='rounded', bgcolor='lightyellow')
    output.node('reports', 'Report Generation\n(CLI/JSON/HTML)')
    output.node('storage', 'Container Storage\nFilesystem Access')

# Add edges
dot.edge('runner', 'libvein', 'manages')
dot.edge('libvein', 'storage', 'inspects')
dot.edge('runner', 'config', 'reads')

# Plugin connections
for plugin in ['malware', 'weakpass', 'mount', 'sensitive', 'cve', 'intrusion']:
    dot.edge('runner', plugin, 'orchestrates')
    dot.edge(plugin, 'reports', 'generates')
    dot.edge(plugin, 'libvein', 'uses')

# Set graph title
dot.attr(label='Veinmind-Tools Architecture\nContainer Security Analysis Platform', labelloc='t', fontsize='16')

# Save the diagram
dot.render('veinmind_architecture', format='png', cleanup=True)