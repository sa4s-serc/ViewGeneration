from graphviz import Digraph

dot = Digraph(comment='Sakura MK I Credit Card BIN Data Service Architecture')
dot.attr(rankdir='TB')

# Add nodes
dot.node('s3', 'S3\nCSV Files', shape='cylinder')
dot.node('lambda1', 'Lambda\nCSV Processor', shape='rectangle')
dot.node('sqs', 'SQS\nMessage Queue', shape='rectangle')
dot.node('lambda2', 'Lambda\nData Transformer', shape='rectangle')
dot.node('dynamo', 'DynamoDB\nBIN Data Store', shape='cylinder')
dot.node('api', 'API Gateway', shape='rectangle')
dot.node('kinesis', 'Kinesis/SQS\nEvent Stream', shape='rectangle')

# Add edges
dot.edge('s3', 'lambda1', 'CSV Files')
dot.edge('lambda1', 'sqs', 'Split Messages')
dot.edge('sqs', 'lambda2', 'Process Messages')
dot.edge('lambda2', 'dynamo', 'Store Data')
dot.edge('api', 'dynamo', 'Query Data')
dot.edge('lambda2', 'kinesis', 'Events')

# Add styling
dot.attr('node', fontname='Arial')
dot.attr('edge', fontname='Arial')
dot.attr(fontname='Arial')
dot.attr(label='Sakura MK I Credit Card BIN Data Service\nServerless Event-Driven Architecture')

# Generate diagram
dot.render('sakura_architecture', format='png', cleanup=True)