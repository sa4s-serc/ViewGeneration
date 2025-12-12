import graphviz

# Create a new directed graph
dot = graphviz.Digraph('OpenShift CAD Architecture', comment='OpenShift Configuration Anomaly Detection System Architecture')
dot.attr(rankdir='TB')

# Define node attributes
dot.attr('node', shape='box', style='filled,rounded', fillcolor='lightgrey', fontname='Arial')

# Core Components
with dot.subgraph(name='cluster_core') as core:
    core.attr(rank='same')
    core.node('pagerduty', 'PagerDuty\nAlerts', fillcolor='lightblue')
    core.node('interceptor', 'Tekton\nInterceptor', fillcolor='lightgreen')
    core.node('pipeline', 'Tekton\nPipelineRuns', fillcolor='lightgreen')
    core.node('cadctl', 'cadctl CLI', fillcolor='orange')

# Investigation Framework
with dot.subgraph(name='cluster_framework') as framework:
    framework.attr(label='Investigation Framework')
    framework.node('inv_framework', 'Investigation\nFramework', fillcolor='yellow')
    
# External Systems
with dot.subgraph(name='cluster_external') as external:
    external.attr(rank='same')
    external.node('ocm', 'OpenShift\nCluster Manager', fillcolor='pink')
    external.node('aws', 'AWS Services', fillcolor='pink')
    external.node('k8s', 'Kubernetes API', fillcolor='pink')

# Ready Made Investigations
with dot.subgraph(name='cluster_investigations') as investigations:
    investigations.attr(label='Ready Made Investigations')
    investigations.node('chgm', 'chgm')
    investigations.node('api', 'apierrorbudgetburn')
    investigations.node('insights', 'insightsoperatordown')
    investigations.node('ccam', 'ccam')
    investigations.node('upgrade', 'upgradeconfigsync')

# Add edges
dot.edge('pagerduty', 'interceptor', 'webhooks')
dot.edge('interceptor', 'pipeline', 'validates')
dot.edge('pipeline', 'cadctl', 'executes')
dot.edge('cadctl', 'inv_framework', 'uses')

# Investigation connections
dot.edge('inv_framework', 'chgm')
dot.edge('inv_framework', 'api')
dot.edge('inv_framework', 'insights')
dot.edge('inv_framework', 'ccam')
dot.edge('inv_framework', 'upgrade')

# External system connections
dot.edge('cadctl', 'ocm', 'cluster info')
dot.edge('cadctl', 'aws', 'cloud trail')
dot.edge('cadctl', 'k8s', 'resources')

# Set graph attributes
dot.attr(fontname='Arial')
dot.attr(rankdir='TB')
dot.attr('edge', fontname='Arial', fontsize='10')

# Save the diagram
dot.render('openshift_cad_architecture', format='png', cleanup=True)