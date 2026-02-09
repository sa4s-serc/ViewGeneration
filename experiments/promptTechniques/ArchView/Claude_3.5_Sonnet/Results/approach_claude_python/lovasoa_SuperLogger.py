from graphviz import Digraph

dot = Digraph(comment='ELK Stack System Monitoring Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Add components
dot.node('agent', 'Java Agent\n(Data Collection)')
dot.node('tcpserver', 'TCP Server\n(Data Transmission)')
dot.node('logstash', 'Logstash\n(Data Processing)')
dot.node('elastic', 'Elasticsearch\n(Storage & Indexing)')
dot.node('kibana', 'Kibana\n(Visualization)')

# Add connections
dot.edge('agent', 'tcpserver', 'System Info')
dot.edge('tcpserver', 'logstash', 'TCP')
dot.edge('logstash', 'elastic', 'JSON Data')
dot.edge('elastic', 'kibana', 'Query/Response')

# Add subgraph for agent components
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Agent Components')
    c.node('sysinfo', 'SystemInfo.java')
    c.node('server', 'TCPServer.java')
    c.edge('sysinfo', 'server')

# Add legend
dot.node('legend', '''Legend:
Component
------------------
Data Flow''', shape='none')

dot.render('elk_stack_architecture', format='png', cleanup=True)