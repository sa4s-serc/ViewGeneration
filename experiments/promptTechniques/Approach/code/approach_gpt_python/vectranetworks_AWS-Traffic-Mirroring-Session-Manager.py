from graphviz import Digraph

dot = Digraph(comment='AWS VPC Traffic Mirroring Automation Tool')

# Main Components
dot.node('tap', 'tap.py (Main Entry Point)')
dot.node('config_vpc', 'config_vpc.py (VPC Configuration)')
dot.node('blacklist', 'blacklist.py / whitelist.py (Instance Lists)')
dot.node('ec2_api_client', 'ec2_api_client.py (EC2 API Abstraction)')
dot.node('spile_tapper', 'spile_tapper.py (Instance Discovery & Session Management)')
dot.node('spile', 'spile.py (Session Management)')
dot.node('tag_config', 'tag_config.py (Tag Management)')
dot.node('nlb_factory', 'nlb_factory.py (NLB Creation)')
dot.node('nlb_target_factory', 'nlb_target_factory.py (Mirror Target Creation)')

# Relationships
dot.edge('tap', 'spile_tapper', label='uses')
dot.edge('tap', 'config_vpc', label='uses')
dot.edge('tap', 'blacklist', label='uses')
dot.edge('spile_tapper', 'ec2_api_client', label='interacts with')
dot.edge('spile_tapper', 'spile', label='delegates session management to')
dot.edge('spile', 'tag_config', label='manages tags with')
dot.edge('spile_tapper', 'nlb_factory', label='uses')
dot.edge('spile_tapper', 'nlb_target_factory', label='uses')

# Additional Styles
dot.attr('node', shape='rectangle', style='filled', color='lightblue')
dot.attr('edge', arrowhead='open')
dot.attr(rankdir='LR')

# Output the diagram
dot.render('aws_vpc_traffic_mirroring_automation_tool', format='png', cleanup=True)