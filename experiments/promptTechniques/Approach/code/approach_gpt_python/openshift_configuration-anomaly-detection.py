from graphviz import Digraph

dot = Digraph(comment='OpenShift CAD System Architecture')

# Define styles
dot.attr('node', shape='rectangle', style='filled', color='lightgrey')
dot.attr('edge', style='bold')

# Components
dot.node('PagerDuty', 'PagerDuty')
dot.node('TektonInterceptor', 'Tekton Interceptor')
dot.node('CADCTL', 'cadctl CLI')
dot.node('TektonPipeline', 'Tekton PipelineRuns')
dot.node('OCM', 'OpenShift Cluster Manager')
dot.node('AWS', 'AWS')
dot.node('Kubernetes', 'Kubernetes')
dot.node('NetworkVerifier', 'osd-network-verifier')
dot.node('Investigation', 'Investigation Plugins')

# External Systems
dot.attr('node', color='lightblue')
dot.node('ExternalPagerDuty', 'PagerDuty (External)')
dot.node('ExternalOCM', 'OCM (External)')
dot.node('ExternalAWS', 'AWS (External)')

# Connections
dot.edge('ExternalPagerDuty', 'PagerDuty', label='Alerts', arrowhead='normal')
dot.edge('PagerDuty', 'TektonInterceptor', label='Webhook', arrowhead='normal')
dot.edge('TektonInterceptor', 'CADCTL', label='Invoke', arrowhead='normal')
dot.edge('CADCTL', 'TektonPipeline', label='Trigger', arrowhead='normal')
dot.edge('CADCTL', 'Investigation', label='Perform', arrowhead='normal')
dot.edge('TektonPipeline', 'Kubernetes', label='Inspect', arrowhead='normal')
dot.edge('TektonPipeline', 'OCM', label='Interact', arrowhead='normal')
dot.edge('TektonPipeline', 'AWS', label='Login/Inspect', arrowhead='normal')
dot.edge('TektonPipeline', 'NetworkVerifier', label='Validate', arrowhead='normal')

# Integrations
dot.edge('ExternalOCM', 'OCM', label='Cluster Info', arrowhead='normal')
dot.edge('ExternalAWS', 'AWS', label='Instance Info', arrowhead='normal')

# Legend
dot.attr('node', shape='plaintext', color='black')
dot.node('legend', '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
    <TR><TD BGCOLOR="lightgrey">Components</TD></TR>
    <TR><TD BGCOLOR="lightblue">External Systems</TD></TR>
</TABLE>>''')

# Render
dot.render('openshift_cad_architecture', format='png', cleanup=True)