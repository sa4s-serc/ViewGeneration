from graphviz import Digraph

dot = Digraph(comment='GKE Pub/Sub WebSocket Adapter Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded')

# Add components
dot.node('pubsub', 'Google Cloud\nPub/Sub')
dot.node('pulltop', 'Pulltop\nContainer')
dot.node('websocketd', 'WebSocketd\nContainer')
dot.node('storage', 'Ephemeral\nPOSIX Storage')
dot.node('cron', 'Cron Job')
dot.node('client', 'WebSocket\nClients')
dot.node('k8s', 'Kubernetes\nCluster')
dot.node('workload', 'Workload\nIdentity')

# Add connections
dot.edge('pubsub', 'pulltop', 'Pull Messages')
dot.edge('pulltop', 'storage', 'Write Messages')
dot.edge('storage', 'websocketd', 'Read Messages')
dot.edge('websocketd', 'client', 'Stream Data')
dot.edge('cron', 'storage', 'Rotate Files')
dot.edge('k8s', 'workload', 'Auth')
dot.edge('workload', 'pubsub', 'Authenticate')

# Cluster for GKE components
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Google Kubernetes Engine')
    c.attr('node', shape='box')
    c.node('pulltop_gke', 'Pulltop')
    c.node('websocketd_gke', 'WebSocketd')
    c.node('storage_gke', 'Storage')
    c.node('cron_gke', 'Cron')

dot.render('gke_pubsub_websocket_adapter', format='png', cleanup=True)