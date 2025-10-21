from graphviz import Digraph

dot = Digraph(comment='ChatGPTClient Android Application MVVM Architecture')

# MVVM Layers
dot.node('M', 'Model', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('V', 'View', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('VM', 'ViewModel', shape='rectangle', style='filled', fillcolor='lightcoral')

# Components within Model
dot.node('DB', 'AppDatabase (Singleton)', shape='rectangle')
dot.node('Repo', 'Repository', shape='rectangle')
dot.node('ChatDao', 'ChatDao (DAO)', shape='rectangle')
dot.node('MsgDao', 'MsgDao (DAO)', shape='rectangle')

# Components within View
dot.node('ChatActivity', 'ChatActivity', shape='rectangle')
dot.node('SettingsActivity', 'SettingsActivity', shape='rectangle')
dot.node('Layouts', 'Layouts', shape='rectangle')

# Components within ViewModel
dot.node('ChatVM', 'ChatViewModel', shape='rectangle')
dot.node('ChatListVM', 'ChatListViewModel', shape='rectangle')
dot.node('MsgListVM', 'MsgListViewModel', shape='rectangle')

# Relationships
dot.edge('DB', 'ChatDao')
dot.edge('DB', 'MsgDao')
dot.edge('Repo', 'ChatDao', dir='both')
dot.edge('Repo', 'MsgDao', dir='both')
dot.edge('VM', 'Repo', label='data access', style='dashed')
dot.edge('ChatVM', 'ChatActivity', dir='both')
dot.edge('ChatListVM', 'ChatActivity', dir='both')
dot.edge('MsgListVM', 'ChatActivity', dir='both')
dot.edge('VM', 'SettingsActivity', label='data binding', style='dashed')
dot.edge('V', 'Layouts', label='UI rendering', style='dashed')

# MVVM Connections
dot.edge('M', 'VM', label='data/model')
dot.edge('VM', 'V', label='updates')

# Data Flow
dot.edge('V', 'VM', label='user input', style='dashed')
dot.edge('VM', 'M', label='model update', style='dashed')

dot.render('chatgptclient_mvvvm_architecture', format='png', cleanup=True)