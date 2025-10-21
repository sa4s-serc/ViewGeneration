from graphviz import Digraph

def generate_diagram():
    dot = Digraph(comment='GoCloud Architecture')

    # Cloud Provider Abstraction
    dot.node('CPA', 'Cloud Provider Abstraction', shape='rect', style='filled', color='lightgrey')

    # Core Services
    dot.node('CS', 'Core Services', shape='rect', style='filled', color='lightblue')
    dot.node('Compute', 'Compute Services', shape='rect')
    dot.node('Storage', 'Storage Services', shape='rect')
    dot.node('Container', 'Container Services', shape='rect')
    dot.node('DNS', 'DNS Services', shape='rect')
    dot.node('LoadBalancer', 'Load Balancing Services', shape='rect')
    dot.node('Serverless', 'Serverless Computing', shape='rect')
    dot.node('Database', 'Database Services', shape='rect')
    dot.node('ML', 'Machine Learning Services', shape='rect')
    dot.node('Analytics', 'Analytics Services', shape='rect')
    dot.node('BareMetal', 'Vultr Bare Metal', shape='rect')
    dot.node('Notification', 'Notification Services', shape='rect')
    dot.node('StreamProcessing', 'Stream Data Processing', shape='rect')
    dot.node('Auth', 'Authentication', shape='rect')

    # Cloud Providers
    dot.node('AWS', 'AWS', shape='rect', style='filled', color='lightcoral')
    dot.node('GoogleCloud', 'Google Cloud', shape='rect', style='filled', color='lightcoral')
    dot.node('DigitalOcean', 'DigitalOcean', shape='rect', style='filled', color='lightcoral')
    dot.node('AliCloud', 'AliCloud', shape='rect', style='filled', color='lightcoral')
    dot.node('Vultr', 'Vultr', shape='rect', style='filled', color='lightcoral')
    dot.node('Rackspace', 'Rackspace', shape='rect', style='filled', color='lightcoral')
    dot.node('Azure', 'Azure', shape='rect', style='filled', color='lightcoral')
    dot.node('OpenStack', 'OpenStack', shape='rect', style='filled', color='lightcoral')

    # Relationships
    dot.edge('CPA', 'CS', label='Uses')
    dot.edge('CS', 'Compute')
    dot.edge('CS', 'Storage')
    dot.edge('CS', 'Container')
    dot.edge('CS', 'DNS')
    dot.edge('CS', 'LoadBalancer')
    dot.edge('CS', 'Serverless')
    dot.edge('CS', 'Database')
    dot.edge('CS', 'ML')
    dot.edge('CS', 'Analytics')
    dot.edge('CS', 'BareMetal')
    dot.edge('CS', 'Notification')
    dot.edge('CS', 'StreamProcessing')
    dot.edge('CS', 'Auth')

    # Provider Connections
    dot.edge('AWS', 'Compute', label='Provides', dir='none')
    dot.edge('GoogleCloud', 'Compute', label='Provides', dir='none')
    dot.edge('DigitalOcean', 'Compute', label='Provides', dir='none')
    dot.edge('AliCloud', 'Compute', label='Provides', dir='none')
    dot.edge('Vultr', 'Compute', label='Provides', dir='none')
    dot.edge('Rackspace', 'Compute', label='Provides', dir='none')
    dot.edge('Azure', 'Compute', label='Provides', dir='none')
    dot.edge('OpenStack', 'Compute', label='Provides', dir='none')

    dot.edge('AWS', 'Storage', label='Provides', dir='none')
    dot.edge('GoogleCloud', 'Storage', label='Provides', dir='none')
    dot.edge('DigitalOcean', 'Storage', label='Provides', dir='none')
    dot.edge('AliCloud', 'Storage', label='Provides', dir='none')
    dot.edge('Vultr', 'Storage', label='Provides', dir='none')
    dot.edge('Rackspace', 'Storage', label='Provides', dir='none')
    dot.edge('Azure', 'Storage', label='Provides', dir='none')
    dot.edge('OpenStack', 'Storage', label='Provides', dir='none')

    dot.edge('AWS', 'Container', label='Provides', dir='none')
    dot.edge('GoogleCloud', 'Container', label='Provides', dir='none')

    # Render diagram
    dot.render('gocloud_architecture', format='png', cleanup=True)

generate_diagram()