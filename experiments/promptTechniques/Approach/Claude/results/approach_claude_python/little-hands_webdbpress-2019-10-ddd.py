from graphviz import Digraph

dot = Digraph(comment='DDD Sample Application Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='rounded')

# Create clusters/subgraphs for layers
with dot.subgraph(name='cluster_0') as app_layer:
    app_layer.attr(label='Application Layer')
    app_layer.node('app_service', 'ScreeningApplicationService\n(v1-v4)')

with dot.subgraph(name='cluster_1') as domain_layer:
    domain_layer.attr(label='Domain Layer')
    domain_layer.node('screening', 'Screening\n(v1-v4)')
    domain_layer.node('interview', 'Interview\n(v1-v4)')
    domain_layer.node('email', 'EmailAddress')
    domain_layer.node('screening_id', 'ScreeningId')
    domain_layer.node('screening_status', 'ScreeningStatus\n(v1-v4)')
    domain_layer.node('interviews', 'Interviews')
    domain_layer.node('step_result', 'ScreeningStepResult')

with dot.subgraph(name='cluster_2') as data_layer:
    data_layer.attr(label='Data Access Layer')
    data_layer.node('screening_dao', 'ScreeningDao')
    data_layer.node('interview_dao', 'InterviewDao')
    data_layer.node('screening_repo', 'ScreeningRepository')
    data_layer.node('screening_jdbc', 'ScreeningJdbcRepository')

# Add edges
dot.edge('app_service', 'screening')
dot.edge('app_service', 'screening_repo')
dot.edge('screening', 'interview')
dot.edge('screening', 'email')
dot.edge('screening', 'screening_id')
dot.edge('screening', 'screening_status')
dot.edge('screening', 'interviews')
dot.edge('screening', 'step_result')
dot.edge('screening_repo', 'screening_jdbc')
dot.edge('screening_jdbc', 'screening_dao')
dot.edge('screening_jdbc', 'interview_dao')

# Set graph attributes
dot.attr(fontname='Helvetica')
dot.attr('node', fontname='Helvetica')
dot.attr('edge', fontname='Helvetica')

# Save the diagram
dot.render('ddd_architecture', format='png', cleanup=True)