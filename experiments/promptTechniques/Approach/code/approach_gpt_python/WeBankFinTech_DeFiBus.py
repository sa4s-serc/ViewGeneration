from graphviz import Digraph

# Initialize the diagram
dot = Digraph(comment='DeFiBus Broker Component Analysis', format='png')

# Define styles for nodes
client_style = {'shape': 'ellipse', 'style': 'filled', 'fillcolor': '#c6e2ff'}
manager_style = {'shape': 'rectangle', 'style': 'filled', 'fillcolor': '#ffcccb'}
processor_style = {'shape': 'rectangle', 'style': 'filled', 'fillcolor': '#98fb98'}
controller_style = {'shape': 'rectangle', 'style': 'filled', 'fillcolor': '#ffebcd'}
other_style = {'shape': 'rectangle', 'style': 'filled', 'fillcolor': '#dcdcdc'}

# Define components
dot.node('A', 'DeFiBrokerController', **controller_style)
dot.node('B', 'DeFiProducerManager', **manager_style)
dot.node('C', 'DeFiConsumerManager', **manager_style)
dot.node('D', 'ConsumeQueueManager', **manager_style)
dot.node('E', 'DeFiSendMessageProcessor', **processor_style)
dot.node('F', 'DeFiReplyMessageProcessor', **processor_style)
dot.node('G', 'DeFiAdminBrokerProcessor', **processor_style)
dot.node('H', 'QueueListeningMonitor', **other_style)
dot.node('I', 'AdjustQueueNumStrategy', **other_style)
dot.node('J', 'MessageRedirectManager', **other_style)
dot.node('K', 'DeFiPluginMessageStore', **other_style)
dot.node('L', 'DeFiPullMessageProcessor', **processor_style)
dot.node('M', 'ClientRebalanceResultManager', **other_style)
dot.node('N', 'DeFiTopicConfigManager', **other_style)
dot.node('O', 'DeFiBusBroker2Client', **client_style)

# Define communication links (uni-directional and bi-directional)
dot.edge('A', 'B', label='manages')
dot.edge('A', 'C', label='manages')
dot.edge('A', 'D', label='manages')
dot.edge('A', 'E', label='initializes')
dot.edge('A', 'F', label='initializes')
dot.edge('A', 'G', label='initializes')
dot.edge('C', 'I', label='uses', dir='both')
dot.edge('C', 'M', label='uses')
dot.edge('B', 'J', label='uses')
dot.edge('D', 'H', label='monitors', dir='both')
dot.edge('D', 'K', label='extends', dir='both')
dot.edge('E', 'L', label='processes', dir='both')
dot.edge('A', 'O', label='communicates', dir='both')

# Render the diagram to a file
dot.render('defibus_broker_component_analysis', view=False)