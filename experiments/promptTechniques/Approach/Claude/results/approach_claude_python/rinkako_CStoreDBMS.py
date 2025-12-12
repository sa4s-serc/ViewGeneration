from graphviz import Digraph

dot = Digraph(comment='CStoreDB Architecture View')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='filled', fillcolor='lightgray')

# Add layers
with dot.subgraph(name='cluster_interface') as interface:
    interface.attr(label='DBInterface Layer')
    interface.node('controller', 'DBController')
    interface.node('connpool', 'DBConnectionPool')

with dot.subgraph(name='cluster_compiler') as compiler:
    compiler.attr(label='DBCompiler Layer')
    compiler.node('lexical', 'LexicalAnalyzer')
    compiler.node('syntax', 'SyntaxParser')
    compiler.node('pile', 'Pile')
    compiler.node('csdb', 'CSDatabase')
    compiler.node('bridge', 'DBBridge')

with dot.subgraph(name='cluster_engine') as engine:
    engine.attr(label='DBEngine Layer')
    engine.node('file_mgr', 'FileManager')
    engine.node('table_mgr', 'TableManager')
    engine.node('allocator', 'DBAllocator')
    engine.node('lock', 'DBLock')
    engine.node('transaction', 'DBTransaction')

# Add connections between components
dot.edge('controller', 'connpool')
dot.edge('connpool', 'bridge')
dot.edge('bridge', 'csdb')
dot.edge('lexical', 'syntax')
dot.edge('syntax', 'pile')
dot.edge('pile', 'csdb')
dot.edge('csdb', 'file_mgr')
dot.edge('csdb', 'table_mgr')
dot.edge('file_mgr', 'allocator')
dot.edge('table_mgr', 'lock')
dot.edge('table_mgr', 'transaction')

# Set graph attributes
dot.attr(overlap='false')
dot.attr(splines='ortho')
dot.attr(nodesep='0.8')
dot.attr(ranksep='1.0')

# Save the diagram
dot.render('cstoredb_architecture', format='png', cleanup=True)