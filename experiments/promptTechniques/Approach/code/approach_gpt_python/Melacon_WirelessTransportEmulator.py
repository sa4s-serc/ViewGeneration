from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='OpenYuma Wireless Transport Emulator')

# Define the style for nodes and edges
node_style = {'shape': 'rect', 'style': 'filled', 'fillcolor': 'lightgrey', 'fontname': 'Arial'}
edge_style = {'fontname': 'Arial'}

# Add nodes for major components
dot.node('DockerContainers', 'Docker Containers', **node_style)
dot.node('NETCONFServer', 'OpenYuma NETCONF Server', **node_style)
dot.node('ConfigMgmt', 'Configuration Management', **node_style)
dot.node('DataModeling', 'Data Modeling and Validation', **node_style)
dot.node('DataConversion', 'Data Conversion and Export', **node_style)
dot.node('TestingInfra', 'Testing Infrastructure', **node_style)
dot.node('SNMPMgmt', 'SNMP Management', **node_style)
dot.node('NotificationHandling', 'Notification Handling', **node_style)
dot.node('ScriptingEngine', 'Scripting Engine', **node_style)
dot.node('CLI', 'CLI Interface (yangcli)', **node_style)

# Define communication paths
dot.edge('DockerContainers', 'NETCONFServer', label='Emulates NEs', **edge_style)
dot.edge('NETCONFServer', 'ConfigMgmt', label='Config via NETCONF', **edge_style)
dot.edge('ConfigMgmt', 'DataModeling', label='Uses YANG Models', **edge_style)
dot.edge('DataModeling', 'DataConversion', label='Converts YANG', **edge_style)
dot.edge('DataModeling', 'TestingInfra', label='Validates Data', **edge_style)
dot.edge('DataModeling', 'SNMPMgmt', label='Provides MIBs', **edge_style)
dot.edge('NETCONFServer', 'NotificationHandling', label='Generates Notifications', **edge_style)
dot.edge('NETCONFServer', 'ScriptingEngine', label='Executes Scripts', **edge_style)
dot.edge('ScriptingEngine', 'CLI', label='Interacts with yangcli', **edge_style)

# Render the graph
dot.render('openyuma_emulator_diagram', format='png', cleanup=True)