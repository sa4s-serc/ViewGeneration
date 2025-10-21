from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='BloSS Core Architecture', format='png')

# Define styles
styles = {
    'graph': {
        'splines': 'ortho',
        'nodesep': '1.0',
        'ranksep': '1.5',
        'fontsize': '10'
    },
    'nodes': {
        'shape': 'record',
        'style': 'filled',
        'fillcolor': 'lightgrey',
        'color': 'black',
        'fontname': 'helvetica',
    },
    'edges': {
        'color': 'black',
        'arrowhead': 'open',
        'fontname': 'helvetica',
    }
}

# Apply styles
dot.graph_attr.update(styles['graph'])
dot.node_attr.update(styles['nodes'])
dot.edge_attr.update(styles['edges'])

# Components
dot.node('Stalk', '''{
    Stalk|
    {Network Traffic Monitoring|Attack Detection}|
    {Ryu SDN Framework|REST API}
}''')

dot.node('Pollen', '''{
    Pollen|
    {Blockchain Integration|Data Storage}|
    {Ethereum|InfluxDB|IPFS}
}''')

dot.node('BloSS', '''{
    BloSS|
    {Mitigation Request Handling|Attack Signaling}|
    {REST API}
}''')

dot.node('Configuration', 'Configuration\n(configuration.py)')
dot.node('Logging', 'Logging\n(logger.py)')
dot.node('Entry Point', 'Entry Point\n(runner.py)')

# Key Files Relationships
dot.edge('Configuration', 'Stalk', label='configures')
dot.edge('Configuration', 'Pollen', label='configures')
dot.edge('Configuration', 'BloSS', label='configures')

dot.edge('Logging', 'Stalk', label='logs')
dot.edge('Logging', 'Pollen', label='logs')
dot.edge('Logging', 'BloSS', label='logs')

dot.edge('Entry Point', 'Stalk', label='initiates')
dot.edge('Entry Point', 'BloSS', label='initiates')

# Interactions
dot.edge('Stalk', 'Pollen', label='reports attacks')
dot.edge('Pollen', 'BloSS', label='triggers mitigation')
dot.edge('BloSS', 'Stalk', label='requests mitigation')

# Render the diagram
dot.render('bloss_core_architecture', view=True)