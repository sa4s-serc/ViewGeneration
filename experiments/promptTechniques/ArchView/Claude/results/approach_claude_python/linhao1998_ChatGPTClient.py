from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='ChatGPTClient Android Architecture')
dot.attr(rankdir='TB')

# Define node and edge styles
dot.attr('node', shape='rectangle', style='filled,rounded', fillcolor='lightgrey')
dot.attr('edge', fontsize='10')

# Create MVVM architecture layers
with dot.subgraph(name='cluster_presentation') as presentation:
    presentation.attr(label='Presentation Layer', style='filled', color='lightblue', fillcolor='lightblue')
    presentation.node('chat_activity', 'ChatActivity')
    presentation.node('settings_activity', 'SettingsActivity')
    presentation.node('chat_adapter', 'ChatAdapter')
    presentation.node('msg_adapter', 'MsgAdapter')

with dot.subgraph(name='cluster_viewmodel') as viewmodel:
    viewmodel.attr(label='ViewModel Layer', style='filled', color='lightgreen', fillcolor='lightgreen')
    viewmodel.node('chat_viewmodel', 'ChatViewModel')
    viewmodel.node('chatlist_viewmodel', 'ChatListViewModel')
    viewmodel.node('msglist_viewmodel', 'MsgListViewModel')

with dot.subgraph(name='cluster_data') as data:
    data.attr(label='Data Layer', style='filled', color='lightyellow', fillcolor='lightyellow')
    data.node('repository', 'Repository')
    data.node('chat_dao', 'ChatDao')
    data.node('msg_dao', 'MsgDao')
    data.node('app_database', 'AppDatabase')

# Add connections between components
dot.edge('chat_activity', 'chat_viewmodel', 'observes')
dot.edge('chat_activity', 'chat_adapter', 'uses')
dot.edge('chat_activity', 'msg_adapter', 'uses')
dot.edge('settings_activity', 'chat_viewmodel', 'observes')

dot.edge('chat_viewmodel', 'repository', 'uses')
dot.edge('chatlist_viewmodel', 'repository', 'uses')
dot.edge('msglist_viewmodel', 'repository', 'uses')

dot.edge('repository', 'chat_dao', 'uses')
dot.edge('repository', 'msg_dao', 'uses')
dot.edge('chat_dao', 'app_database', 'accesses')
dot.edge('msg_dao', 'app_database', 'accesses')

# Save the diagram
dot.render('chatgpt_client_architecture', format='png', cleanup=True)