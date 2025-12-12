from graphviz import Digraph

dot = Digraph(comment='Matrix Chatbot Architecture')
dot.attr(rankdir='TB', size='8,10')

with dot.subgraph(name='cluster_external') as c:
    c.attr(label='External Systems', style='dashed', color='blue')
    c.node('matrix_homeserver', 'Matrix Homeserver', shape='cylinder')
    c.node('user', 'User', shape='ellipse')

with dot.subgraph(name='cluster_modules') as c:
    c.attr(label='Chatbot Modules', style='filled', color='lightgrey')
    c.node('main', 'main.py\n(Entry Point)', shape='ellipse')
    c.node('message_eval', 'message_evaluation.py\n(Intent Detection)', shape='box')
    c.node('nlp', 'nlp.py\n(Text Processing)', shape='box')
    c.node('response_mgmt', 'response_management.py\n(Response Generation)', shape='box')
    c.node('index_eval', 'index_evaluation.py\n(Web Scraping)', shape='box')
    c.node('small_talk', 'small_talk_evaluation.py\n(Small Talk)', shape='box')
    c.node('org_eval', 'organisation_evaluation.py\n(Org Data)', shape='box')

with dot.subgraph(name='cluster_services') as c:
    c.attr(label='Services', style='filled', color='lightblue')
    c.node('db_service', 'database_service.py\n(Data Access)', shape='box')

with dot.subgraph(name='cluster_data') as c:
    c.attr(label='Data & Configuration', style='filled', color='lightyellow')
    c.node('config', 'config.py\n(Configuration)', shape='note')
    c.node('postgres', 'PostgreSQL\n(Knowledge Base)', shape='cylinder')
    c.node('org_txt', 'organisation.txt\n(Org Data)', shape='note')
    c.node('small_talk_txt', 'small_talk.txt\n(Small Talk)', shape='note')

dot.edge('user', 'matrix_homeserver', label='Sends Message')
dot.edge('matrix_homeserver', 'main', label='Event Callback')
dot.edge('main', 'message_eval', label='Process Message')
dot.edge('message_eval', 'nlp', label='Text for Processing')
dot.edge('nlp', 'message_eval', label='Processed Text')
dot.edge('message_eval', 'db_service', label='Query Knowledge')
dot.edge('db_service', 'postgres', label='SQL Queries')
dot.edge('postgres', 'db_service', label='Query Results')
dot.edge('db_service', 'message_eval', label='Retrieved Data')
dot.edge('message_eval', 'response_mgmt', label='Evaluation Results')
dot.edge('response_mgmt', 'main', label='Formulated Response')
dot.edge('main', 'matrix_homeserver', label='Send Response')
dot.edge('index_eval', 'db_service', label='Store Scraped Data')
dot.edge('small_talk', 'db_service', label='Add Small Talk')
dot.edge('org_eval', 'db_service', label='Add Org Data')
dot.edge('org_txt', 'org_eval', label='Read Data')
dot.edge('small_talk_txt', 'small_talk', label='Read Data')
dot.edge('config', 'main', label='Configuration')
dot.edge('config', 'db_service', label='DB Config')

dot.render('matrix_chatbot_architecture', format='png', cleanup=True)