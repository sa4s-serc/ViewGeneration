from graphviz import Digraph

# Create a Digraph object
dot = Digraph(comment='FEC ERegulations Architecture')

# Add nodes for core components
dot.node('DjangoApp', 'Django Application', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('DB', 'PostgreSQL Database', shape='cylinder', style='filled', fillcolor='lightgreen')
dot.node('ES', 'ElasticSearch', shape='cylinder', style='filled', fillcolor='lightgreen')
dot.node('CF', 'Cloud Foundry', shape='rectangle', style='filled', fillcolor='lightyellow')
dot.node('API', 'External API', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('CMS', 'Content Management System', shape='rectangle', style='filled', fillcolor='lightgrey')

# Add subcomponents
dot.node('RegCore', 'Regulations Core', shape='ellipse', style='filled', fillcolor='lightcoral')
dot.node('RegSite', 'Regulations Site', shape='ellipse', style='filled', fillcolor='lightcoral')
dot.node('RegParser', 'Regulations Parser', shape='ellipse', style='filled', fillcolor='lightcoral')
dot.node('ERegsExt', 'ERegs Extensions', shape='ellipse', style='filled', fillcolor='lightcoral')

# Connect components
dot.edge('DjangoApp', 'DB', label='MPTT Structure')
dot.edge('DjangoApp', 'ES', label='Keyword Search')
dot.edge('DjangoApp', 'CF', label='Deployment')
dot.edge('DjangoApp', 'API', label='Data Fetch')
dot.edge('DjangoApp', 'CMS', label='Content Management')
dot.edge('DjangoApp', 'RegCore', label='Data Model')
dot.edge('DjangoApp', 'RegSite', label='UI Components')
dot.edge('DjangoApp', 'RegParser', label='Parsing Logic')
dot.edge('DjangoApp', 'ERegsExt', label='Custom Extensions')

# Add legend
dot.node('Legend', 'Legend', shape='plaintext')
dot.node('Component', 'Component', shape='rectangle', style='filled', fillcolor='lightblue')
dot.node('Database', 'Database', shape='cylinder', style='filled', fillcolor='lightgreen')
dot.node('Service', 'Service', shape='rectangle', style='filled', fillcolor='lightgrey')
dot.node('Subsystem', 'Subsystem', shape='ellipse', style='filled', fillcolor='lightcoral')

dot.edge('Legend', 'Component', style='invis')
dot.edge('Legend', 'Database', style='invis')
dot.edge('Legend', 'Service', style='invis')
dot.edge('Legend', 'Subsystem', style='invis')

# Render the diagram
dot.render('fec_eregs_architecture', view=True)