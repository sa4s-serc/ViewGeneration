import graphviz

dot = graphviz.Digraph(comment='Veinmind-Tools Architecture')
dot.attr(rankdir='TB', size='8,10')

# Core Components
with dot.subgraph(name='cluster_core') as core:
    core.attr(label='Core Components', style='filled', color='lightgrey')
    core.node('libveinmind', 'libveinmind\n(Container Runtime Interface)', shape='box', style='filled', color='lightblue')
    core.node('runner', 'veinmind-runner\n(Plugin Orchestrator)', shape='box', style='filled', color='lightblue')
    core.node('common', 'veinmind-common-go\n(Common Library)', shape='box', style='filled', color='lightblue')

# Plugin Components
with dot.subgraph(name='cluster_plugins') as plugins:
    plugins.attr(label='Security Plugins', style='filled', color='lightyellow')
    plugins.node('weakpass', 'Weak Password Scanner', shape='box')
    plugins.node('sensitive', 'Sensitive Data Scanner', shape='box')
    plugins.node('malware', 'Malicious File Detector', shape='box')
    plugins.node('cve', 'CVE Vulnerability Scanner', shape='box')
    plugins.node('intrusion', 'Intrusion Trace Detector', shape='box')
    plugins.node('mount', 'Unsafe Mount Detector', shape='box')

# Infrastructure Components
with dot.subgraph(name='cluster_infra') as infra:
    infra.attr(label='Infrastructure', style='filled', color='lightgreen')
    infra.node('ci_cd', 'CI/CD Pipeline\n(GitHub Actions)', shape='box')
    infra.node('docker', 'Docker Containers', shape='box')
    infra.node('config', 'TOML Configuration', shape='box')
    infra.node('git', 'Git Repository', shape='box')

# External Components
dot.node('container_runtime', 'Container Runtime', shape='cylinder')
dot.node('filesystem', 'Container Filesystem', shape='cylinder')
dot.node('reports', 'Report Generation\n(CLI/JSON/HTML)', shape='ellipse')

# Core connections
dot.edge('runner', 'libveinmind', label='uses')
dot.edge('runner', 'common', label='uses')
dot.edge('libveinmind', 'container_runtime', label='inspects')
dot.edge('libveinmind', 'filesystem', label='accesses')

# Plugin connections
dot.edge('runner', 'weakpass', label='orchestrates')
dot.edge('runner', 'sensitive', label='orchestrates')
dot.edge('runner', 'malware', label='orchestrates')
dot.edge('runner', 'cve', label='orchestrates')
dot.edge('runner', 'intrusion', label='orchestrates')
dot.edge('runner', 'mount', label='orchestrates')

# Plugin to core connections
dot.edge('weakpass', 'libveinmind', style='dashed')
dot.edge('sensitive', 'libveinmind', style='dashed')
dot.edge('malware', 'libveinmind', style='dashed')
dot.edge('cve', 'libveinmind', style='dashed')
dot.edge('intrusion', 'libveinmind', style='dashed')
dot.edge('mount', 'libveinmind', style='dashed')

# Infrastructure connections
dot.edge('ci_cd', 'docker', label='builds')
dot.edge('ci_cd', 'git', label='clones')
dot.edge('runner', 'config', label='reads')
dot.edge('plugins', 'config', style='dashed', label='configured by')

# Output connections
dot.edge('runner', 'reports', label='generates')
dot.edge('plugins', 'reports', style='dashed', label='contribute to')

dot.render('veinmind_architecture', format='png', cleanup=True)