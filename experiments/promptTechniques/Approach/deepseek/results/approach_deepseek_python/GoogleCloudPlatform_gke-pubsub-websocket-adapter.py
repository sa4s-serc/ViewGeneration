import graphviz

dot = graphviz.Digraph(comment='GKE PubSub Websocket Adapter Architecture')
dot.attr(rankdir='TB', size='8,8')

# Define nodes with styles
dot.node('pubsub', 'Google Cloud Pub/Sub', shape='cylinder', style='filled', fillcolor='lightblue')
dot.node('gke', 'GKE Cluster', shape='folder', style='filled', fillcolor='lightgrey')
dot.node('pulltop', 'pulltop\nCLI Tool', shape='box', style='filled', fillcolor='lightgreen')
dot.node('websocketd', 'websocketd\nWebSocket Server', shape='box', style='filled', fillcolor='lightgreen')
dot.node('storage', 'Ephemeral POSIX Storage\n(Message Buffer)', shape='note', style='filled', fillcolor='lightyellow')
dot.node('cron', 'Cron Job\n(File Rotation)', shape='box', style='filled', fillcolor='lightcoral')
dot.node('client', 'WebSocket Client\n(Web Application)', shape='box', style='filled', fillcolor='lightpink')
dot.node('workload_identity', 'Workload Identity', shape='ellipse', style='filled', fillcolor='lightcyan')

# Define edges
dot.edge('pubsub', 'pulltop', label='Pull Messages', style='solid')
dot.edge('pulltop', 'storage', label='Write Messages', style='solid')
dot.edge('storage', 'websocketd', label='Read Messages', style='solid')
dot.edge('websocketd', 'client', label='WebSocket Stream', style='solid')
dot.edge('cron', 'storage', label='Rotate Files', style='dashed')
dot.edge('workload_identity', 'pulltop', label='Authentication', style='dotted')

# Group GKE components
with dot.subgraph(name='cluster_gke') as c:
    c.attr(label='GKE Pod', style='dashed', color='blue')
    c.node('pulltop')
    c.node('websocketd')
    c.node('storage')
    c.node('cron')

dot.render('gke_pubsub_websocket_adapter_architecture', format='png', cleanup=True)