from graphviz import Digraph

dot = Digraph(comment='Tarzan Distributed Transaction System')

# Define nodes
dot.node('Server', 'Server\n- Manages configurations\n- Schedules tasks', shape='rectangle')
dot.node('Client', 'Client\n- Sends messages\n- Handles transactions', shape='rectangle')
dot.node('Registry', 'Registry\n- Zookeeper based\n- Service discovery', shape='rectangle')
dot.node('MessageBroker', 'Message Broker\n- RocketMQ', shape='rectangle')
dot.node('TarzanMQ', 'Tarzan MQ\n- RocketMQ integration', shape='rectangle')
dot.node('TarzanRegistry', 'Tarzan Registry\n- Service registration', shape='rectangle')
dot.node('TarzanServer', 'Tarzan Server\n- Core server module', shape='rectangle')
dot.node('TarzanRPC', 'Tarzan RPC\n- Netty based RPC', shape='rectangle')
dot.node('TarzanCommon', 'Tarzan Common\n- Common utilities', shape='rectangle')
dot.node('TarzanStore', 'Tarzan Store\n- Data storage and management', shape='rectangle')
dot.node('TarzanCluster', 'Tarzan Cluster\n- Clustering strategies', shape='rectangle')
dot.node('TarzanExample', 'Tarzan Example\n- Client library usage', shape='rectangle')
dot.node('Database', 'Database\n- MySQL', shape='rectangle')
dot.node('Redis', 'Redis\n- Distributed locks', shape='rectangle')

# Define edges
dot.edge('Client', 'Server', label='Message Sending', arrowhead='open', style='dashed')
dot.edge('Server', 'MessageBroker', label='Message Proxying', arrowhead='open', style='dashed')
dot.edge('Server', 'Registry', label='Service Discovery', arrowhead='open', style='dashed')
dot.edge('Server', 'TarzanStore', label='Data Management', arrowhead='open', style='dashed')
dot.edge('TarzanStore', 'Database', label='Persistence', arrowhead='open', style='dashed')
dot.edge('TarzanStore', 'Redis', label='Distributed Locks', arrowhead='open', style='dashed')
dot.edge('TarzanMQ', 'MessageBroker', label='Integration', arrowhead='open', style='dashed')
dot.edge('TarzanServer', 'TarzanCommon', label='Utilities', arrowhead='open', style='dashed')
dot.edge('TarzanRegistry', 'Registry', label='Zookeeper Integration', arrowhead='open', style='dashed')
dot.edge('TarzanRPC', 'TarzanServer', label='RPC Communication', arrowhead='open', style='dashed')
dot.edge('TarzanCluster', 'TarzanServer', label='Load Balancing', arrowhead='open', style='dashed')

# Render the graph
dot.format = 'png'
dot.render('tarzan_distributed_transaction_system_diagram', view=True)