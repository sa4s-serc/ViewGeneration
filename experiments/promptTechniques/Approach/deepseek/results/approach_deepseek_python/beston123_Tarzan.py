import graphviz

dot = graphviz.Digraph(comment='Tarzan Distributed Transaction System Architecture')
dot.attr(rankdir='TB', size='8,10')

# Main components
with dot.subgraph(name='cluster_client') as c:
    c.attr(label='Client Layer', style='filled', color='lightblue')
    c.node('client', 'Client', shape='rectangle')

with dot.subgraph(name='cluster_server') as s:
    s.attr(label='Server Layer', style='filled', color='lightgreen')
    s.node('server', 'Server', shape='rectangle')
    s.node('config_manager', 'Config Manager', shape='rectangle')
    s.node('scheduled_service', 'Scheduled Service Manager', shape='rectangle')
    s.node('message_resend', 'Message Resend Service', shape='rectangle')
    s.node('server_controller', 'Server Controller', shape='rectangle')

with dot.subgraph(name='cluster_registry') as r:
    r.attr(label='Registry Layer', style='filled', color='lightyellow')
    r.node('zookeeper', 'Zookeeper Registry', shape='rectangle')

with dot.subgraph(name='cluster_mq') as m:
    m.attr(label='Message Queue Layer', style='filled', color='lightpink')
    m.node('rocketmq', 'RocketMQ', shape='rectangle')
    m.node('mq_notifier', 'RocketMQ Message Notifier', shape='rectangle')
    m.node('mq_checker', 'RocketMQ Transaction Checker', shape='rectangle')

with dot.subgraph(name='cluster_store') as st:
    st.attr(label='Data Storage Layer', style='filled', color='lightcoral')
    st.node('store_service', 'RocketMQ Store Service', shape='rectangle')
    st.node('mysql', 'MySQL Database', shape='cylinder')
    st.node('redis', 'Redis', shape='cylinder')

with dot.subgraph(name='cluster_rpc') as rpc:
    rpc.attr(label='RPC Layer', style='filled', color='lightgray')
    rpc.node('rpc_client', 'RPC Client', shape='rectangle')
    rpc.node('rpc_server', 'RPC Server', shape='rectangle')

# Connections
dot.edge('client', 'server', label='Sends Messages')
dot.edge('server', 'zookeeper', label='Service Discovery')
dot.edge('server', 'rocketmq', label='Proxies Messages')
dot.edge('server', 'store_service', label='Stores Transaction Data')
dot.edge('server', 'rpc_server', label='Handles RPC Requests')
dot.edge('client', 'rpc_client', label='RPC Communication')
dot.edge('scheduled_service', 'redis', label='Distributed Locks')
dot.edge('message_resend', 'rocketmq', label='Resend Failed Messages')
dot.edge('mq_notifier', 'rocketmq', label='Message Notification')
dot.edge('mq_checker', 'rocketmq', label='Transaction Status Check')
dot.edge('store_service', 'mysql', label='Data Persistence')
dot.edge('store_service', 'redis', label='Cache & Locks')

# Internal server connections
dot.edge('server', 'config_manager', style='dashed')
dot.edge('server', 'scheduled_service', style='dashed')
dot.edge('server', 'message_resend', style='dashed')
dot.edge('server', 'server_controller', style='dashed')

dot.render('tarzan_architecture', format='png', cleanup=True)