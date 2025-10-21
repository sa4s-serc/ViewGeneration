from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Domain-Driven Design Sample Application')

# Define styles
styles = {
    'graph': {
        'label': 'Domain-Driven Design Sample Application',
        'fontsize': '16',
        'fontcolor': 'black',
        'bgcolor': 'white',
        'rankdir': 'LR',
    },
    'nodes': {
        'fontname': 'Helvetica',
        'shape': 'rectangle',
        'fontcolor': 'black',
        'color': 'black',
        'style': 'filled',
        'fillcolor': '#b3cde0',
    },
    'edges': {
        'style': 'solid',
        'color': 'black',
        'arrowhead': 'open',
        'fontname': 'Courier',
        'fontsize': '12',
        'fontcolor': 'black',
    }
}

# Apply styles
dot.attr(**styles['graph'])
dot.attr('node', **styles['nodes'])
dot.attr('edge', **styles['edges'])

# Add nodes for layers
dot.node('Domain Layer', 'Domain Layer')
dot.node('Application Services', 'Application Services')
dot.node('Data Access Layer', 'Data Access Layer')

# Add subcomponents within Domain Layer
dot.node('ScreeningV1', 'ScreeningV1')
dot.node('ScreeningV4', 'ScreeningV4')
dot.node('InterviewV1', 'InterviewV1')
dot.node('InterviewV4', 'InterviewV4')
dot.node('EmailAddress', 'EmailAddress')
dot.node('ScreeningId', 'ScreeningId')

# Add subcomponents within Application Services
dot.node('ScreeningApplicationServiceV1', 'ScreeningApplicationServiceV1')
dot.node('ScreeningApplicationServiceV4', 'ScreeningApplicationServiceV4')

# Add subcomponents within Data Access Layer
dot.node('ScreeningDao', 'ScreeningDao')
dot.node('InterviewDao', 'InterviewDao')
dot.node('ScreeningRepository', 'ScreeningRepository')
dot.node('ScreeningJdbcRepository', 'ScreeningJdbcRepository')

# Add edges between layers
dot.edge('Application Services', 'Domain Layer')
dot.edge('Domain Layer', 'Data Access Layer')

# Add edges for Domain Layer subcomponents
dot.edge('ScreeningV1', 'ScreeningV4')
dot.edge('InterviewV1', 'InterviewV4')
dot.edge('ScreeningV4', 'EmailAddress')
dot.edge('ScreeningV4', 'ScreeningId')

# Add edges for Application Services subcomponents
dot.edge('ScreeningApplicationServiceV1', 'ScreeningApplicationServiceV4')

# Add edges for Data Access Layer subcomponents
dot.edge('ScreeningDao', 'ScreeningRepository')
dot.edge('InterviewDao', 'ScreeningJdbcRepository')

# Add edges between specific components
dot.edge('ScreeningApplicationServiceV1', 'ScreeningV1')
dot.edge('ScreeningApplicationServiceV4', 'ScreeningV4')
dot.edge('ScreeningV1', 'ScreeningDao')
dot.edge('ScreeningV4', 'ScreeningJdbcRepository')

# Save the source code and render the graph
dot.render('ddd_sample_application', format='png', cleanup=True)