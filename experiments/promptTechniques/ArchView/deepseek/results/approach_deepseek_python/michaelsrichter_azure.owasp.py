import graphviz

dot = graphviz.Digraph(comment='Architectural View')
dot.attr(rankdir='TB')

with dot.subgraph(name='cluster_web_apps') as web_apps:
    web_apps.attr(label='Web Applications', style='filled', color='lightgrey')
    web_apps.node('asp_net_ad', 'ASP.NET MVC App\n(Azure AD Groups)', shape='rectangle')
    web_apps.node('asp_net_insecure', 'ASP.NET MVC App\n(Insecure)', shape='rectangle')
    web_apps.node('node_express', 'Node.js Express App', shape='rectangle')

with dot.subgraph(name='cluster_waf') as waf:
    waf.attr(label='Web Application Firewall', style='filled', color='lightblue')
    waf.node('modsecurity', 'ModSecurity\nwith CRS', shape='component')
    waf.node('barracuda', 'Barracuda WAF', shape='component')

with dot.subgraph(name='cluster_deployment') as deployment:
    deployment.attr(label='Azure Deployment', style='filled', color='lightgreen')
    deployment.node('arm_templates', 'ARM Templates', shape='folder')
    deployment.node('powershell', 'PowerShell Scripts', shape='ellipse')

with dot.subgraph(name='cluster_client') as client:
    client.attr(label='Client-Side Libraries', style='filled', color='lightyellow')
    client.node('jquery', 'jQuery', shape='rectangle')
    client.node('bootstrap', 'Bootstrap', shape='rectangle')
    client.node('modernizr', 'Modernizr', shape='rectangle')

dot.edge('client', 'asp_net_ad', label='HTTP/HTTPS')
dot.edge('client', 'asp_net_insecure', label='HTTP/HTTPS')
dot.edge('client', 'node_express', label='HTTP/HTTPS')
dot.edge('modsecurity', 'asp_net_ad', label='Protects', style='dashed')
dot.edge('modsecurity', 'asp_net_insecure', label='Protects', style='dashed')
dot.edge('barracuda', 'node_express', label='Protects', style='dashed')
dot.edge('arm_templates', 'asp_net_ad', label='Deploys', style='dotted')
dot.edge('arm_templates', 'asp_net_insecure', label='Deploys', style='dotted')
dot.edge('arm_templates', 'node_express', label='Deploys', style='dotted')
dot.edge('powershell', 'arm_templates', label='Executes', style='dotted')

dot.render('architecture_view', format='png', cleanup=True)