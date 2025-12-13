import graphviz

dot = graphviz.Digraph(comment='AWS VPC Traffic Mirroring Automation Tool Architecture')
dot.attr(rankdir='TB', size='8,10')

# Main components
dot.node('tap', 'tap.py\n(Main Entry Point)', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('config_vpc', 'config_vpc.py\n(VPC Configuration)', shape='rectangle', style='filled', fillcolor='lightcoral')
dot.node('ec2_api_client', 'ec2_api_client.py\n(EC2 API Abstraction)', shape='rectangle', style='filled', fillcolor='lightgreen')
dot.node('spile_tapper', 'spile_tapper.py\n(Instance Discovery &\nSession Management)', shape='rectangle', style='filled', fillcolor='lightyellow')
dot.node('spile', 'spile.py\n(Session Management)', shape='rectangle', style='filled', fillcolor='lightpink')
dot.node('tag_config', 'tag_config.py\n(Tag Management)', shape='rectangle', style='filled', fillcolor='lightgray')
dot.node('nlb_factory', 'nlb_factory.py\n(NLB Creation)', shape='rectangle', style='filled', fillcolor='lightcyan')
dot.node('nlb_target_factory', 'nlb_target_factory.py\n(Mirror Target Creation)', shape='rectangle', style='filled', fillcolor='wheat')
dot.node('blacklist', 'blacklist.py\n(Instance Blacklist)', shape='rectangle', style='filled', fillcolor='mistyrose')
dot.node('whitelist', 'whitelist.py\n(Instance Whitelist)', shape='rectangle', style='filled', fillcolor='honeydew')

# AWS Resources
dot.node('aws_vpc', 'AWS VPC', shape='ellipse', style='filled', fillcolor='orange')
dot.node('aws_ec2', 'EC2 Instances', shape='ellipse', style='filled', fillcolor='orange')
dot.node('aws_tags', 'AWS Tags', shape='ellipse', style='filled', fillcolor='orange')
dot.node('nlb_target', 'NLB/ENI\nMirror Targets', shape='ellipse', style='filled', fillcolor='orange')

# Relationships
dot.edge('tap', 'config_vpc', label='configures')
dot.edge('tap', 'spile_tapper', label='invokes')
dot.edge('config_vpc', 'aws_tags', label='reads/writes')
dot.edge('ec2_api_client', 'aws_ec2', label='queries')
dot.edge('ec2_api_client', 'aws_tags', label='manages')
dot.edge('spile_tapper', 'ec2_api_client', label='uses')
dot.edge('spile_tapper', 'spile', label='delegates to')
dot.edge('spile_tapper', 'aws_vpc', label='discovers instances in')
dot.edge('spile', 'nlb_factory', label='requests NLB')
dot.edge('spile', 'nlb_target_factory', label='requests target')
dot.edge('spile', 'aws_ec2', label='manages sessions on')
dot.edge('tag_config', 'aws_tags', label='serializes/validates')
dot.edge('nlb_factory', 'nlb_target', label='creates')
dot.edge('nlb_target_factory', 'nlb_target', label='creates')
dot.edge('blacklist', 'aws_tags', label='manages')
dot.edge('whitelist', 'aws_tags', label='manages')

# Design pattern annotations
with dot.subgraph(name='cluster_patterns') as c:
    c.attr(label='Design Patterns', style='dashed')
    c.node('facade', 'Facade Pattern\n(EC2ApiClient)', shape='note')
    c.node('factory', 'Factory Pattern\n(NLB factories)', shape='note')
    c.node('strategy', 'Strategy Pattern\n(Enrollment modes)', shape='note')
    c.node('dto', 'DTO Pattern\n(namedtuples)', shape='note')

dot.edge('facade', 'ec2_api_client', style='dashed')
dot.edge('factory', 'nlb_factory', style='dashed')
dot.edge('factory', 'nlb_target_factory', style='dashed')
dot.edge('strategy', 'spile', style='dashed')
dot.edge('dto', 'tag_config', style='dashed')

dot.render('aws_vpc_traffic_mirroring_architecture', format='png', cleanup=True)