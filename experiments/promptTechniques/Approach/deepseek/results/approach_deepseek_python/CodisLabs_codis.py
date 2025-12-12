import graphviz

dot = graphviz.Digraph(comment='Architectural View')
dot.attr(rankdir='TB')

with dot.subgraph(name='cluster_redis') as c:
    c.attr(label='Redis Core', style='filled', color='lightgrey')
    c.node('server', 'server.h', shape='box')
    c.node('ae', 'ae (Event Loop)', shape='box')
    c.node('zmalloc', 'zmalloc', shape='box')
    c.node('rio', 'rio', shape='box')
    c.node('networking', 'Networking', shape='box')
    c.node('config', 'Config', shape='box')

with dot.subgraph(name='cluster_data_structures') as c:
    c.attr(label='Data Structures', style='filled', color='lightblue')
    c.node('sds', 'SDS', shape='box')
    c.node('dict', 'Hash Tables', shape='box')
    c.node('list', 'Linked Lists', shape='box')
    c.node('skiplist', 'Skip Lists', shape='box')
    c.node('intset', 'IntSet', shape='box')
    c.node('ziplist', 'Ziplist', shape='box')
    c.node('quicklist', 'Quicklist', shape='box')

with dot.subgraph(name='cluster_persistence') as c:
    c.attr(label='Persistence', style='filled', color='lightgreen')
    c.node('rdb', 'RDB', shape='box')
    c.node('aof', 'AOF', shape='box')
    c.node('lzf', 'LZF Compression', shape='box')

with dot.subgraph(name='cluster_concurrency') as c:
    c.attr(label='Concurrency', style='filled', color='lightyellow')
    c.node('bio', 'BIO System', shape='box')
    c.node('event_loop', 'Event Loop', shape='box')

with dot.subgraph(name='cluster_extensions') as c:
    c.attr(label='Extensions', style='filled', color='lightpink')
    c.node('lua', 'Lua Scripting', shape='box')
    c.node('hiredis', 'hiredis', shape='box')
    c.node('jemalloc', 'jemalloc', shape='box')

with dot.subgraph(name='cluster_cluster') as c:
    c.attr(label='Cluster Management', style='filled', color='lightcyan')
    c.node('codis', 'Codis Proxy', shape='box')
    c.node('sentinel', 'Sentinel', shape='box')
    c.node('gossip', 'Gossip Protocol', shape='box')
    c.node('slots', 'Slots Management', shape='box')

dot.edge('server', 'ae')
dot.edge('server', 'zmalloc')
dot.edge('server', 'rio')
dot.edge('server', 'networking')
dot.edge('server', 'config')
dot.edge('server', 'sds')
dot.edge('server', 'dict')
dot.edge('server', 'list')
dot.edge('server', 'skiplist')
dot.edge('server', 'intset')
dot.edge('server', 'ziplist')
dot.edge('server', 'quicklist')
dot.edge('server', 'rdb')
dot.edge('server', 'aof')
dot.edge('server', 'lzf')
dot.edge('server', 'bio')
dot.edge('server', 'event_loop')
dot.edge('server', 'lua')
dot.edge('server', 'hiredis')
dot.edge('server', 'jemalloc')
dot.edge('server', 'codis')
dot.edge('server', 'sentinel')
dot.edge('server', 'gossip')
dot.edge('server', 'slots')

dot.render('architectural_view', format='png', cleanup=True)