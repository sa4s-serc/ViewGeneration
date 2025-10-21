from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='Azure Web Application Security Architecture')

# Define nodes for core components
dot.node('A', 'ASP.NET MVC App - Secure')
dot.node('B', 'ASP.NET MVC App - Insecure')
dot.node('C', 'Node.js Express App')
dot.node('D', 'ModSecurity CRS')
dot.node('E', 'Barracuda WAF')
dot.node('F', 'Azure AD')
dot.node('G', 'Azure Resources\n(VMs, Load Balancers)')
dot.node('H', 'ARM Templates')
dot.node('I', 'PowerShell Scripts')
dot.node('J', 'Client-side Libraries\n(jQuery, Bootstrap)')

# Define edges representing interactions and data flow
dot.edge('A', 'F', label='Auth via Azure AD')
dot.edge('B', 'E', label='Protected by WAF')
dot.edge('C', 'E', label='Protected by WAF')
dot.edge('D', 'E', label='WAF Rules')
dot.edge('E', 'G', label='Traffic Routed')
dot.edge('H', 'G', label='Provision Resources')
dot.edge('I', 'H', label='Deploy ARM Templates')
dot.edge('J', 'A', label='Enhance UI')
dot.edge('J', 'B', label='Enhance UI')

# Visualize WAF and ModSecurity as a subsystem
with dot.subgraph(name='cluster_0') as c:
    c.attr(style='filled', color='lightgrey')
    c.node_attr.update(style='filled', color='white')
    c.edges([('D', 'E')])
    c.attr(label='Web Application Firewall')

# Save and render the graph
dot.render('azure_web_app_security_architecture', format='png', cleanup=True)
print(dot.source)