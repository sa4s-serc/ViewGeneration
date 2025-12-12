from graphviz import Digraph

# Creating a Digraph object
dot = Digraph(comment='Sakura MK I Credit Card BIN Data Service', format='png')

# Define styles for different component types
styles = {
    'AWS Lambda': 'style=filled, fillcolor=lightblue, shape=rect',
    'DynamoDB': 'style=filled, fillcolor=lightgreen, shape=cylinder',
    'API Gateway': 'style=filled, fillcolor=lightyellow, shape=rect',
    'S3': 'style=filled, fillcolor=lightgrey, shape=cylinder',
    'Kinesis/SQS': 'style=filled, fillcolor=lightpink, shape=rect'
}

# Adding nodes for each component
dot.node('S3', 'S3', **{'style':'filled', 'fillcolor':'lightgrey', 'shape':'cylinder'})
dot.node('Kinesis/SQS', 'Kinesis/SQS', **{'style':'filled', 'fillcolor':'lightpink', 'shape':'rect'})
dot.node('Lambda1', 'AWS Lambda\n(CSV Ingestion)', **{'style':'filled', 'fillcolor':'lightblue', 'shape':'rect'})
dot.node('Lambda2', 'AWS Lambda\n(Data Processing)', **{'style':'filled', 'fillcolor':'lightblue', 'shape':'rect'})
dot.node('DynamoDB', 'DynamoDB', **{'style':'filled', 'fillcolor':'lightgreen', 'shape':'cylinder'})
dot.node('APIGateway', 'API Gateway', **{'style':'filled', 'fillcolor':'lightyellow', 'shape':'rect'})

# Adding edges to represent data flow
dot.edge('S3', 'Kinesis/SQS', label='New CSV File', arrowhead='vee')
dot.edge('Kinesis/SQS', 'Lambda1', label='Trigger', arrowhead='vee')
dot.edge('Lambda1', 'Lambda2', label='Process Messages', arrowhead='vee')
dot.edge('Lambda2', 'DynamoDB', label='Store Processed Data', arrowhead='vee')
dot.edge('APIGateway', 'Lambda2', label='API Call', arrowhead='vee')

# Render the diagram
dot.render('sakura_mk1_credit_card_bin_service_diagram')