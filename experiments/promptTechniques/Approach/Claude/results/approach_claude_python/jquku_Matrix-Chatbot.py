from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Matrix Chatbot Architecture')
dot.attr(rankdir='TB', splines='ortho')

# Define node styles
dot.attr('node', shape='rectangle', style='filled,rounded', fillcolor='lightgray', fontname='Arial')
dot.attr('edge', fontname='Arial', fontsize='10')

# Create subgraph for core components
with dot.subgraph(name='cluster_0') as core:
    core.attr(label='Core Components', style='rounded', color='blue')
    
    core.node('matrix_client', 'Matrix Client\n(matrix-nio)', shape='component')
    core.node('chatbot_core', 'Chatbot Core', shape='component')
    core.node('nlp', 'NLP Pipeline\n(nltk, autocorrect)', shape='component')
    core.node('msg_eval', 'Message Evaluation', shape='component')
    core.node('resp_mgmt', 'Response Management', shape='component')

# Create subgraph for data layer
with dot.subgraph(name='cluster_1') as data:
    data.attr(label='Data Layer', style='rounded', color='green')
    
    data.node('db_service', 'Database Service\n(psycopg2)', shape='cylinder')
    data.node('postgres', 'PostgreSQL', shape='cylinder')
    data.node('config', 'Config\n(YAML)', shape='note')

# Create subgraph for knowledge domains
with dot.subgraph(name='cluster_2') as knowledge:
    knowledge.attr(label='Knowledge Domains', style='rounded', color='red')
    
    knowledge.node('small_talk', 'Small Talk', shape='folder')
    knowledge.node('org_info', 'Organization Info', shape='folder')
    knowledge.node('web_index', 'Web Indices', shape='folder')

# Add connections
# Core component connections
dot.edge('matrix_client', 'chatbot_core')
dot.edge('chatbot_core', 'nlp')
dot.edge('nlp', 'msg_eval')
dot.edge('msg_eval', 'resp_mgmt')
dot.edge('resp_mgmt', 'chatbot_core')

# Data layer connections
dot.edge('db_service', 'postgres')
dot.edge('config', 'chatbot_core')
dot.edge('config', 'db_service')

# Knowledge domain connections
dot.edge('small_talk', 'postgres')
dot.edge('org_info', 'postgres')
dot.edge('web_index', 'postgres')
dot.edge('msg_eval', 'db_service')
dot.edge('resp_mgmt', 'db_service')

# Add some styling
dot.attr(bgcolor='white')
dot.attr('node', margin='0.2')

# Save the diagram
dot.render('matrix_chatbot_architecture', format='png', cleanup=True)