from graphviz import Digraph

dot = Digraph('Architecture Overview')
dot.attr(rankdir='TB')

# Define node styles
dot.attr('node', shape='rectangle', style='rounded')

# Create main components
dot.node('web_app', 'ASP.NET MVC Web Applications\n(Secure & Insecure Demos)')
dot.node('waf', 'Web Application Firewall\n(ModSecurity + OWASP CRS)')
dot.node('azure_ad', 'Azure AD Integration\n(Authentication & Groups)')
dot.node('node_app', 'Node.js Express App')
dot.node('crs', 'ModSecurity Core Rule Set')
dot.node('arm', 'Azure Resource Manager\nTemplates')
dot.node('scripts', 'PowerShell Deployment\nScripts')
dot.node('client', 'Client-Side Libraries\n(jQuery, Bootstrap)')

# Define relationships
dot.edge('client', 'web_app', 'HTTP/HTTPS')
dot.edge('client', 'node_app', 'HTTP/HTTPS')
dot.edge('web_app', 'waf', 'Protected by')
dot.edge('node_app', 'waf', 'Protected by')
dot.edge('waf', 'crs', 'Uses')
dot.edge('web_app', 'azure_ad', 'Authenticates via')
dot.edge('arm', 'scripts', 'Deployed by')
dot.edge('scripts', 'web_app', 'Provisions')
dot.edge('scripts', 'waf', 'Configures')

# Add subgraph for security components
with dot.subgraph(name='cluster_security') as sec:
    sec.attr(label='Security Layer')
    sec.node('sec_rules', 'Security Rules\n(XSS, LFI, RFI)')
    sec.edge('crs', 'sec_rules', 'Implements')

dot.render('architecture_diagram', format='png', cleanup=True)