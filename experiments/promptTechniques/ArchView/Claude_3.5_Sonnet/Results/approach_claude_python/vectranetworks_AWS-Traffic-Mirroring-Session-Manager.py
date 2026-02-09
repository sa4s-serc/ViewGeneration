from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='AWS VPC Traffic Mirroring Architecture')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='box', style='filled,rounded', fillcolor='lightgray', fontname='Arial')

# Create clusters for logical grouping
with dot.subgraph(name='cluster_0') as c:
    c.attr(label='Core Components', style='rounded', color='blue')
    c.node('tap', 'tap.py\nMain Entry Point')
    c.node('spile_tapper', 'spile_tapper.py\nInstance Discovery')
    c.node('spile', 'spile.py\nSession Management')

with dot.subgraph(name='cluster_1') as c:
    c.attr(label='Configuration', style='rounded', color='green')
    c.node('config_vpc', 'config_vpc.py\nVPC Configuration')
    c.node('tag_config', 'tag_config.py\nTag Management')
    c.node('blacklist', 'blacklist.py\nInstance Lists')
    c.node('whitelist', 'whitelist.py\nInstance Lists')

with dot.subgraph(name='cluster_2') as c:
    c.attr(label='AWS Integration', style='rounded', color='orange')
    c.node('ec2_api', 'ec2_api_client.py\nEC2 API Abstraction')
    c.node('nlb_factory', 'nlb_factory.py\nNLB Creation')
    c.node('nlb_target', 'nlb_target_factory.py\nMirror Target Creation')

# Add relationships
dot.edge('tap', 'config_vpc', 'configures')
dot.edge('tap', 'spile_tapper', 'manages')
dot.edge('config_vpc', 'tag_config', 'uses')
dot.edge('config_vpc', 'ec2_api', 'queries')
dot.edge('blacklist', 'tag_config', 'updates')
dot.edge('whitelist', 'tag_config', 'updates')
dot.edge('spile_tapper', 'spile', 'creates')
dot.edge('spile_tapper', 'ec2_api', 'discovers')
dot.edge('spile', 'nlb_factory', 'creates')
dot.edge('spile', 'nlb_target', 'configures')
dot.edge('spile', 'tag_config', 'manages')
dot.edge('nlb_factory', 'ec2_api', 'uses')
dot.edge('nlb_target', 'ec2_api', 'uses')

# Set graph attributes
dot.attr(fontsize='16')
dot.attr('edge', fontsize='10')

# Save the diagram
dot.render('aws_vpc_traffic_mirroring_architecture', format='png', cleanup=True)