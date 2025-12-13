from graphviz import Digraph

dot = Digraph(comment='Audit Framework Analysis: auditor-v1')

# Setting the style of the graph
dot.attr(rankdir='LR', size='10', style='filled', color='lightgrey', fontsize='12', fontname='Helvetica')

# Defining nodes
dot.node('A', 'Client Library', shape='box', style='filled', color='lightblue')
dot.node('B', 'Application Server', shape='box', style='filled', color='lightblue')
dot.node('C', 'ConsumerService', shape='ellipse', style='filled', color='lightyellow')
dot.node('D', 'AuditEventRepositoryService', shape='ellipse', style='filled', color='lightyellow')
dot.node('E', 'Kafka', shape='cylinder', style='filled', color='lightgreen')
dot.node('F', 'Elasticsearch', shape='cylinder', style='filled', color='lightgreen')

# Defining edges
dot.edge('A', 'E', label='Event Streaming', color='black')
dot.edge('E', 'C', label='Subscribe to Kafka topics', color='black')
dot.edge('C', 'D', label='Persist Events', color='black')
dot.edge('D', 'F', label='Store in Elasticsearch', color='black')

# Adding metadata
dot.attr(label='auditor-v1 Architecture\nFocus: Scalability, Maintainability\nStyle: Event-Driven Microservices', fontsize='14')

# Rendering the graph
dot.render('audit_framework_analysis', format='png', cleanup=True)