from graphviz import Digraph

dot = Digraph(comment='Elasticsearch-SpringBoot Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded', fontname='Arial')

# Create clusters/subgraphs for layers
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Client Layer')
    c.node('web_ui', 'Web UI\n(Thymeleaf)')
    c.node('rest_client', 'REST Client')

with dot.subgraph(name='cluster_1') as c:
    c.attr(label='Controller Layer')
    c.node('admin_ctrl', 'Admin Controller')
    c.node('api_ctrl', 'API Controller')

with dot.subgraph(name='cluster_2') as c:
    c.attr(label='Service Layer')
    c.node('index_service', 'Index Service')

with dot.subgraph(name='cluster_3') as c:
    c.attr(label='Repository Layer')
    c.node('jdbc_repo', 'JDBC Repository')
    c.node('es_client', 'Elasticsearch Client')

with dot.subgraph(name='cluster_4') as c:
    c.attr(label='Data Layer')
    c.node('mysql', 'MySQL')
    c.node('elasticsearch', 'Elasticsearch')

# Define relationships
dot.edge('web_ui', 'admin_ctrl')
dot.edge('rest_client', 'api_ctrl')
dot.edge('admin_ctrl', 'index_service')
dot.edge('api_ctrl', 'index_service')
dot.edge('index_service', 'jdbc_repo')
dot.edge('index_service', 'es_client')
dot.edge('jdbc_repo', 'mysql')
dot.edge('es_client', 'elasticsearch')

# Save the diagram
dot.render('elasticsearch_springboot_architecture', format='png', cleanup=True)