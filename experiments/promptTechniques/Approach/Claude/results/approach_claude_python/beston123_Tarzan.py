from graphviz import Digraph

dot = Digraph(comment='Tarzan Distributed Transaction System Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded,filled', fillcolor='lightgrey')

# Create main components
dot.node('server', 'Server\n(Message Proxy, Config Management)')
dot.node('client', 'Client\n(Transaction Management)')
dot.node('registry', 'Registry\n(Zookeeper)')
dot.node('mq', 'Message Broker\n(RocketMQ)')
dot.node('store', 'Data Store\n(MySQL, Redis)')

# Create subcomponents
with dot.subgraph(name='cluster_server') as c:
    c.attr(label='Server Components')
    c.node('config_mgr', 'Config Manager')
    c.node('sched_mgr', 'Scheduled Service Manager')
    c.node('msg_resend', 'Message Resend Service')
    c.node('server_ctrl', 'Server Controller')

# Create connections
dot.edge('client', 'server', 'Send Messages')
dot.edge('server', 'mq', 'Proxy Messages')
dot.edge('server', 'registry', 'Service Discovery')
dot.edge('server', 'store', 'Persist Data')
dot.edge('mq', 'client', 'Message Delivery')

# Connect subcomponents
dot.edge('server', 'config_mgr')
dot.edge('server', 'sched_mgr')
dot.edge('server', 'msg_resend')
dot.edge('server', 'server_ctrl')

# Print the source code
print(dot.source)

# Save the diagram
dot.render('tarzan_architecture', format='png', cleanup=True)