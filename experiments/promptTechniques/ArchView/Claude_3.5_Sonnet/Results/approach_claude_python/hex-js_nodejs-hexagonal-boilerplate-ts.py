from graphviz import Digraph

dot = Digraph('hexagonal_architecture')
dot.attr(rankdir='TB')

# Styling
dot.attr('node', shape='box', style='filled', fillcolor='lightgray')
dot.attr('graph', pad='0.5', nodesep='0.5', ranksep='0.75')

# Core Domain (Hexagon Center)
with dot.subgraph(name='cluster_core') as core:
    core.attr(label='Core Domain', style='filled', color='lightblue', fillcolor='white')
    core.node('business_logic', 'Business Logic\n(src/business/*)')
    core.node('models', 'Domain Models\n(src/models/*)')

# Primary Adapters (Left Side)
with dot.subgraph(name='cluster_primary') as primary:
    primary.attr(label='Primary Adapters', style='filled', color='lightgreen', fillcolor='white')
    primary.node('http_adapter', 'HTTP Controller\n(src/ports/http/*)')
    primary.node('lambda_adapter', 'Lambda Handler\n(src/ports/aws-lambda/*)')

# Secondary Adapters (Right Side)
with dot.subgraph(name='cluster_secondary') as secondary:
    secondary.attr(label='Secondary Adapters', style='filled', color='lightsalmon', fillcolor='white')
    secondary.node('dynamo_adapter', 'DynamoDB Repository\n(src/ports/aws-dynamo/*)')
    secondary.node('sqs_adapter', 'SQS Handler\n(src/ports/aws-sqs/*)')
    secondary.node('logger_adapter', 'Logger\n(src/ports/logger/*)')

# External Systems
with dot.subgraph(name='cluster_external') as external:
    external.attr(label='External Systems', style='filled', color='gray', fillcolor='white')
    external.node('dynamodb', 'AWS DynamoDB')
    external.node('sqs', 'AWS SQS')
    external.node('clients', 'HTTP Clients')

# Core relationships
dot.edge('business_logic', 'models', dir='both')

# Primary adapter relationships
dot.edge('http_adapter', 'business_logic')
dot.edge('lambda_adapter', 'business_logic')
dot.edge('clients', 'http_adapter')

# Secondary adapter relationships
dot.edge('business_logic', 'dynamo_adapter')
dot.edge('business_logic', 'sqs_adapter')
dot.edge('business_logic', 'logger_adapter')
dot.edge('dynamo_adapter', 'dynamodb')
dot.edge('sqs_adapter', 'sqs')

# Factory pattern
dot.node('adapter_factory', 'Adapter Factory\n(todoAdapterFactory)')
dot.edge('adapter_factory', 'dynamo_adapter')
dot.edge('adapter_factory', 'sqs_adapter')

# Save the diagram
dot.render('hexagonal_architecture', view=True, format='png')