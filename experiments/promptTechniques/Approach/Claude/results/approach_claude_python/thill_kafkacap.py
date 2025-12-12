import graphviz

# Create a new directed graph
dot = graphviz.Digraph(comment='KafkaCap Architecture')
dot.attr(rankdir='TB')
dot.attr('node', shape='box', style='rounded')

# Add nodes for main components
with dot.subgraph(name='cluster_capture') as capture:
    capture.attr(label='Capture Layer')
    capture.node('aeron', 'Aeron\nCapture Device')
    capture.node('multicast', 'Multicast\nCapture Device')
    capture.node('websocket', 'Websocket\nCapture Device')
    
# Add Kafka topics layer
with dot.subgraph(name='cluster_kafka') as kafka:
    kafka.attr(label='Kafka Layer')
    kafka.node('kafka_topics', 'Kafka Capture Topics')
    kafka.node('kafka_out', 'Kafka Output Topic')

# Add processing layer
with dot.subgraph(name='cluster_processing') as proc:
    proc.attr(label='Processing Layer')
    proc.node('deduplicator', 'Deduplicator\nConsumer Group')
    proc.node('dedup_strategy', 'Dedup Strategy')
    proc.node('capture_queue', 'Capture Queue')
    proc.node('buffered_pub', 'Buffered Publisher')
    proc.node('recovery', 'Recovery Service')

# Add edges
dot.edge('aeron', 'kafka_topics')
dot.edge('multicast', 'kafka_topics')
dot.edge('websocket', 'kafka_topics')
dot.edge('kafka_topics', 'deduplicator')
dot.edge('deduplicator', 'dedup_strategy')
dot.edge('dedup_strategy', 'capture_queue')
dot.edge('capture_queue', 'buffered_pub')
dot.edge('buffered_pub', 'kafka_out')
dot.edge('kafka_out', 'recovery')
dot.edge('recovery', 'deduplicator')

# Set graph attributes
dot.attr(fontsize='16')
dot.attr('node', fontsize='12')
dot.attr('edge', fontsize='10')

# Render the graph
dot.render('kafkacap_architecture', format='png', cleanup=True)