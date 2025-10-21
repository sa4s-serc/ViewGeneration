from graphviz import Digraph

dot = Digraph(comment='Fabric Gateway Architecture', format='png')

# Define styles
dot.attr('node', shape='rect', style='filled', color='lightgrey', fontname='Helvetica')
dot.attr('edge', fontname='Helvetica', arrowsize='0.8')

# Components
dot.node('CRD', 'FabricGateway CRD')
dot.node('Ingress', 'Ingress Management')
dot.node('Policy', 'Policy Enforcement')
dot.node('ServiceDiscovery', 'Service Discovery')
dot.node('Validation', 'Validation')
dot.node('Search', 'Search')
dot.node('E2ETesting', 'End-to-End Testing')
dot.node('LicenseManagement', 'License Management')
dot.node('Security', 'Security')

# Technology Integration
dot.node('Kubernetes', 'Kubernetes', shape='ellipse', color='lightblue')
dot.node('Skipper', 'Skipper', shape='ellipse', color='lightblue')
dot.node('IAM', 'Zalando IAM', shape='ellipse', color='lightblue')
dot.node('RxJS', 'RxJS', shape='ellipse', color='lightblue')

# Key Files
dot.node('IngressDerivation', 'IngressDerivationChain.scala', shape='note', color='lightyellow')
dot.node('StackSetOps', 'StackSetOperations.scala', shape='note', color='lightyellow')
dot.node('WebhookRoutes', 'GatewayWebhookRoutes.scala', shape='note', color='lightyellow')
dot.node('delivery', 'delivery.yaml', shape='note', color='lightyellow')
dot.node('makeSite', 'make-site.sh', shape='note', color='lightyellow')

# Relationships
dot.edge('CRD', 'Ingress', label='configures')
dot.edge('CRD', 'Policy', label='defines')
dot.edge('CRD', 'Validation', label='validates')
dot.edge('Search', 'RxJS', label='uses')
dot.edge('Ingress', 'Kubernetes', label='integrates')
dot.edge('Ingress', 'Skipper', label='built on')
dot.edge('Policy', 'IAM', label='integrates with')
dot.edge('ServiceDiscovery', 'Kubernetes', label='adapts to')
dot.edge('E2ETesting', 'Kubernetes', label='deploys on')
dot.edge('Security', 'IAM', label='manages')
dot.edge('Ingress', 'IngressDerivation', label='core logic')
dot.edge('ServiceDiscovery', 'StackSetOps', label='handles')
dot.edge('Validation', 'WebhookRoutes', label='defines')
dot.edge('LicenseManagement', 'delivery', label='tracks')
dot.edge('E2ETesting', 'makeSite', label='builds')

# Scope and View
dot.attr(label=r'\nFabric Gateway Architecture\n', fontsize='20', fontname='Helvetica-Bold')

# Render the diagram
dot.render('fabric_gateway_architecture')