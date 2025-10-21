from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='GKE PubSub WebSocket Adapter')

# Define styles
dot.attr('node', shape='rectangle', style='filled', color='lightgrey')
dot.attr('edge', style='dashed', color='black')

# Components
dot.node('GKE', 'Google Kubernetes Engine')
dot.node('PubSub', 'Google Cloud Pub/Sub')
dot.node('Pulltop', 'Pulltop (CLI Tool)', color='lightblue')
dot.node('Websocketd', 'Websocketd (CLI Tool)', color='lightblue')
dot.node('Storage', 'Ephemeral POSIX Storage', color='lightyellow')
dot.node('Cron', 'Cron Job', color='lightblue')
dot.node('WebApp', 'Web Application', color='lightgreen')

# Connections
dot.edge('PubSub', 'Pulltop', label='Pull Messages')
dot.edge('Pulltop', 'Websocketd', label='Expose as WebSocket')
dot.edge('Websocketd', 'WebApp', label='WebSocket Connection')
dot.edge('Websocketd', 'Storage', label='Buffer Messages')
dot.edge('Storage', 'Websocketd', label='Serve Buffered Messages')
dot.edge('Cron', 'Storage', label='Rotate Output JSON')

# System context
dot.edge('GKE', 'Pulltop')
dot.edge('GKE', 'Websocketd')
dot.edge('GKE', 'Cron')

# Render the graph to a file
dot.render('gke_pubsub_websocket_adapter_diagram', view=True, format='png')