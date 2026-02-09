import graphviz

# Create a new directed graph
dot = graphviz.Digraph(comment='DeFiBus Broker Architecture')
dot.attr(rankdir='TB')
dot.attr(compound='true')
dot.attr(fontname='Arial')

# Cluster for Core Components
with dot.subgraph(name='cluster_core') as core:
    core.attr(label='Core Components', style='rounded', bgcolor='lightgrey')
    core.node('broker_controller', 'DeFiBrokerController', shape='rectangle', style='filled', fillcolor='lightblue')
    core.node('msg_store', 'DeFiPluginMessageStore', shape='cylinder', style='filled', fillcolor='palegreen')

# Cluster for Message Processors
with dot.subgraph(name='cluster_processors') as proc:
    proc.attr(label='Message Processors', style='rounded')
    proc.node('send_proc', 'DeFiSendMessageProcessor', shape='rectangle')
    proc.node('reply_proc', 'DeFiReplyMessageProcessor', shape='rectangle')
    proc.node('pull_proc', 'DeFiPullMessageProcessor', shape='rectangle')
    proc.node('admin_proc', 'DeFiAdminBrokerProcessor', shape='rectangle')

# Cluster for Managers
with dot.subgraph(name='cluster_managers') as mgr:
    mgr.attr(label='Management Layer', style='rounded')
    mgr.node('consumer_mgr', 'DeFiConsumerManager', shape='rectangle')
    mgr.node('producer_mgr', 'DeFiProducerManager', shape='rectangle')
    mgr.node('queue_mgr', 'ConsumeQueueManager', shape='rectangle')
    mgr.node('redirect_mgr', 'MessageRedirectManager', shape='rectangle')
    mgr.node('topic_mgr', 'DeFiTopicConfigManager', shape='rectangle')

# Core controller connections
dot.edge('broker_controller', 'send_proc')
dot.edge('broker_controller', 'reply_proc')
dot.edge('broker_controller', 'pull_proc')
dot.edge('broker_controller', 'admin_proc')
dot.edge('broker_controller', 'consumer_mgr')
dot.edge('broker_controller', 'producer_mgr')
dot.edge('broker_controller', 'queue_mgr')
dot.edge('broker_controller', 'redirect_mgr')
dot.edge('broker_controller', 'topic_mgr')

# Message store connections
dot.edge('send_proc', 'msg_store')
dot.edge('reply_proc', 'msg_store')
dot.edge('pull_proc', 'msg_store')
dot.edge('queue_mgr', 'msg_store')

# Manager interconnections
dot.edge('consumer_mgr', 'queue_mgr')
dot.edge('producer_mgr', 'queue_mgr')
dot.edge('redirect_mgr', 'queue_mgr')
dot.edge('topic_mgr', 'queue_mgr')

# Set graph attributes
dot.attr(fontsize='10')
dot.attr(ranksep='0.75')
dot.attr(nodesep='0.5')
dot.attr(pad='0.5')

# Save the diagram
dot.render('defibus_architecture', format='png', cleanup=True)