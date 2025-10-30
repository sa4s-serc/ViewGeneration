from graphviz import Digraph

dot = Digraph(comment='DeFiBus Broker Component Architecture')

# Define nodes
dot.node('DBC', 'DeFiBrokerController')
dot.node('DPM', 'DeFiProducerManager')
dot.node('DCM', 'DeFiConsumerManager')
dot.node('CQM', 'ConsumeQueueManager')
dot.node('DSP', 'DeFiSendMessageProcessor')
dot.node('DRP', 'DeFiReplyMessageProcessor')
dot.node('DABP', 'DeFiAdminBrokerProcessor')
dot.node('QLM', 'QueueListeningMonitor')
dot.node('AQNS', 'AdjustQueueNumStrategy')
dot.node('MRM', 'MessageRedirectManager')
dot.node('DPMS', 'DeFiPluginMessageStore')
dot.node('DPMP', 'DeFiPullMessageProcessor')
dot.node('CRRM', 'ClientRebalanceResultManager')
dot.node('DTCM', 'DeFiTopicConfigManager')
dot.node('DB2C', 'DeFiBusBroker2Client')

# Define edges with correct syntax
edges = [
    ('DBC', 'DPM'),
    ('DBC', 'DCM'),
    ('DBC', 'CQM'),
    ('DBC', 'DSP'),
    ('DBC', 'DRP'),
    ('DBC', 'DABP'),
    ('DBC', 'QLM'),
    ('DBC', 'AQNS'),
    ('DBC', 'MRM'),
    ('DBC', 'DPMS'),
    ('DBC', 'DPMP'),
    ('DBC', 'CRRM'),
    ('DBC', 'DTCM'),
    ('DBC', 'DB2C')
]

for edge in edges:
    dot.edge(edge[0], edge[1])

# Define styles
dot.attr(rankdir='LR', size='10,5')
dot.attr('node', shape='rectangle', style='filled', color='lightgrey')
dot.attr('edge', arrowsize='1.5', color='black')

# Render diagram
dot.render('defibus_broker_architecture', format='png', cleanup=True)