import graphviz as gv

# Create a new directed graph
dot = gv.Digraph(comment='Ivy Wallet Architecture')
dot.attr(rankdir='TB')
dot.attr('node', shape='box', style='rounded')
dot.attr('graph', fontname='Arial', fontsize='12')
dot.attr('edge', fontname='Arial', fontsize='10')

# Define clusters for main layers
with dot.subgraph(name='cluster_0') as s0:
    s0.attr(label='UI Layer', style='filled', color='lightblue', fontname='Arial Bold')
    s0.node('compose_ui', 'Jetpack Compose UI\nComponents')
    s0.node('view_models', 'ViewModels')
    s0.node('design_system', 'Design System')
    s0.edge('compose_ui', 'view_models')
    s0.edge('design_system', 'compose_ui')

with dot.subgraph(name='cluster_1') as s1:
    s1.attr(label='Domain Layer', style='filled', color='lightgreen')
    s1.node('trans_flow', 'Transaction Flow')
    s1.node('account_act', 'Account Actions')
    s1.node('category_act', 'Category Actions')
    s1.node('sync_act', 'Sync Actions')
    s1.node('formula_eng', 'Formula Engine')
    s1.node('backup_act', 'Backup Actions')

with dot.subgraph(name='cluster_2') as s2:
    s2.attr(label='Data Layer', style='filled', color='lightyellow')
    s2.node('local_db', 'Room Database')
    s2.node('remote_backup', 'Remote Backup\n(Google Drive)')
    s2.node('exchange_rates', 'Exchange Rates')
    s2.edge('local_db', 'remote_backup', dir='both')
    s2.edge('exchange_rates', 'local_db')

# Cross-layer connections
dot.edge('view_models', 'trans_flow')
dot.edge('view_models', 'account_act')
dot.edge('view_models', 'category_act')
dot.edge('view_models', 'sync_act')
dot.edge('view_models', 'formula_eng')

dot.edge('trans_flow', 'local_db')
dot.edge('account_act', 'local_db')
dot.edge('category_act', 'local_db')
dot.edge('sync_act', 'remote_backup')
dot.edge('formula_eng', 'local_db')
dot.edge('backup_act', 'remote_backup')

# Add legend
with dot.subgraph(name='cluster_legend') as legend:
    legend.attr(label='Legend', style='filled', color='lightgray')
    legend.node('ui_leg', 'UI Components', style='filled', color='lightblue')
    legend.node('domain_leg', 'Domain Components', style='filled', color='lightgreen')
    legend.node('data_leg', 'Data Components', style='filled', color='lightyellow')

# Save the diagram
dot.render('ivy_wallet_architecture', format='png', cleanup=True)