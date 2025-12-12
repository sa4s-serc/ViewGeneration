from graphviz import Digraph

dot = Digraph(comment='HikariKeeper Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add system components
dot.node('client', 'HikariKeeper Client\n(hikarikeeper-client)')
dot.node('springboot', 'Spring Boot Starter\n(hikarikeeper-springboot-starter)')
dot.node('server', 'HikariKeeper Server\n(hikarikeeper-server)')
dot.node('core', 'Core Module\n(hikarikeeper-core)')
dot.node('discovery', 'Discovery Service')
dot.node('storage', 'Storage Layer\n(RocksDB)')
dot.node('raft', 'Raft Consensus')

# Add subcomponents
with dot.subgraph(name='cluster_core') as c:
    c.attr(label='Core Components')
    c.node('leader', 'Leader Node')
    c.node('follower', 'Follower Node')
    c.node('candidate', 'Candidate Node')
    c.node('log', 'Raft Log')
    c.node('repo', 'Node Repository')

# Add connections
dot.edge('client', 'server', 'Client API')
dot.edge('springboot', 'client', 'Integration')
dot.edge('server', 'core', 'Uses')
dot.edge('core', 'raft', 'Implements')
dot.edge('core', 'storage', 'Persists Data')
dot.edge('core', 'discovery', 'Service Discovery')

# Add core component connections
dot.edge('raft', 'leader', 'Election')
dot.edge('raft', 'follower', 'Replication')
dot.edge('raft', 'candidate', 'Voting')
dot.edge('leader', 'log', 'Manages')
dot.edge('follower', 'log', 'Replicates')
dot.edge('raft', 'repo', 'Persists State')

# Generate diagram
dot.render('hikarikeeper_architecture', format='png', cleanup=True)