from graphviz import Digraph

dot = Digraph(comment='OpenYuma Wireless Transport Emulator Architecture')
dot.attr(rankdir='TB')

# Set styles
dot.attr('node', shape='rectangle', style='rounded')
dot.attr('edge', fontsize='10')

# Define main components
dot.node('netconf', 'OpenYuma NETCONF Server\n(TR-532 Standard)')
dot.node('docker', 'Docker Container\nNetwork Elements')
dot.node('veth', 'VETH Pairs\nLink Emulation')
dot.node('config', 'Configuration Management')
dot.node('yang', 'YANG Data Models')
dot.node('sil', 'Server Instrumentation\nLayer (SIL)')
dot.node('test', 'Testing Framework')
dot.node('notify', 'Notification System')
dot.node('snmp', 'SNMP Management')

# Define subcomponents
with dot.subgraph(name='cluster_0') as config_cluster:
    config_cluster.attr(label='Configuration Components')
    config_cluster.node('topology', 'topology.json')
    config_cluster.node('config_json', 'config.json')
    config_cluster.node('xml_config', 'XML Configs')

# Define relationships
dot.edge('netconf', 'docker', 'manages')
dot.edge('docker', 'veth', 'connects via')
dot.edge('yang', 'netconf', 'defines model')
dot.edge('config', 'netconf', 'configures')
dot.edge('sil', 'netconf', 'implements')
dot.edge('netconf', 'notify', 'generates')
dot.edge('netconf', 'snmp', 'interfaces')
dot.edge('test', 'sil', 'validates')

# Connect configuration components
dot.edge('topology', 'config')
dot.edge('config_json', 'config')
dot.edge('xml_config', 'config')

print(dot.source)
dot.render('openyuma_architecture', view=True, format='png')