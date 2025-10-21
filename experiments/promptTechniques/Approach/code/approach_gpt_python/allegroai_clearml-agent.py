from graphviz import Digraph

dot = Digraph(comment='ClearML Agent Architecture')

# Define styles for different types of nodes
styles = {
    'ClearML Agent': {'shape': 'box', 'style': 'filled', 'color': 'lightblue'},
    'ClearML Server': {'shape': 'box', 'style': 'filled', 'color': 'lightgrey'},
    'ResourceMonitor': {'shape': 'box', 'style': 'filled', 'color': 'lightgreen'},
    'RequirementsManager': {'shape': 'box', 'style': 'filled', 'color': 'lightyellow'},
    'Docker Integration': {'shape': 'box', 'style': 'filled', 'color': 'lightpink'},
    'K8s/SLURM Integration': {'shape': 'box', 'style': 'filled', 'color': 'lightcoral'},
    'Configuration System': {'shape': 'box', 'style': 'filled', 'color': 'lightcyan'}
}

# Add nodes
dot.node('A', 'ClearML Agent', **styles['ClearML Agent'])
dot.node('B', 'ClearML Server', **styles['ClearML Server'])
dot.node('C', 'ResourceMonitor', **styles['ResourceMonitor'])
dot.node('D', 'RequirementsManager', **styles['RequirementsManager'])
dot.node('E', 'Docker Integration', **styles['Docker Integration'])
dot.node('F', 'K8s/SLURM Integration', **styles['K8s/SLURM Integration'])
dot.node('G', 'Configuration System', **styles['Configuration System'])

# Add edges
dot.edge('A', 'B', label='API Communication')
dot.edge('A', 'C', label='Resource Stats Reporting')
dot.edge('A', 'D', label='Manage Dependencies')
dot.edge('A', 'E', label='Docker Management')
dot.edge('A', 'F', label='Integrate with K8s/SLURM')
dot.edge('A', 'G', label='Configuration')

# Add additional interactions
dot.edge('C', 'A', label='Resource Monitoring')
dot.edge('D', 'A', label='Dependencies Management')
dot.edge('E', 'A', label='Container Execution')
dot.edge('F', 'A', label='Job Submission')

dot.render('clearml_agent_architecture', format='png', cleanup=True)