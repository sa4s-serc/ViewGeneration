from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Microservices Architecture of TweetDeck Clone')

# Define nodes for microservices
dot.node('A', 'APIGateway')
dot.node('B', 'AuthFront')
dot.node('C', 'AuthServer')
dot.node('D', 'DataPipeline')
dot.node('E', 'DataProcessing')
dot.node('F', 'DataSending')
dot.node('G', 'UserActivity')

# Define nodes for external systems
dot.node('H', 'Twitter API', shape='cylinder')
dot.node('I', 'Cassandra', shape='cylinder')
dot.node('J', 'Kafka', shape='cylinder')
dot.node('K', 'Spark', shape='cylinder')
dot.node('L', 'Redis', shape='cylinder')

# Define edges between nodes to represent interactions
dot.edge('A', 'B', label='JWT Validation')
dot.edge('B', 'C', label='User Auth')
dot.edge('C', 'L', label='Store Tokens')
dot.edge('A', 'D', label='Route Data')
dot.edge('D', 'J', label='Ingest Data')
dot.edge('J', 'E', label='Process Data')
dot.edge('E', 'K', label='Analyze Data')
dot.edge('K', 'I', label='Store Processed Data')
dot.edge('F', 'I', label='Fetch Data')
dot.edge('F', 'A', label='Send Data')
dot.edge('G', 'A', label='User Interaction')
dot.edge('H', 'D', label='Stream Data')

# Visualize the diagram
dot.attr(rankdir='LR', size='8,5')
dot.render('microservices_architecture', format='png', cleanup=True)