from graphviz import Digraph

def create_jupyterhub_architecture():
    # Create a new directed graph
    dot = Digraph('JupyterHub_OpenShift_Architecture')
    dot.attr(rankdir='TB')
    
    # Define node attributes for different component types
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial')
    
    # Cluster for OpenShift Infrastructure
    with dot.subgraph(name='cluster_openshift') as c:
        c.attr(label='OpenShift Cluster', style='rounded', color='darkgrey')
        
        # Infrastructure components
        c.node('auth', 'Active Directory/LDAP\nAuthentication', fillcolor='lightblue')
        c.node('jupyterhub', 'JupyterHub Server', fillcolor='lightgreen')
        c.node('kubespawner', 'KubeSpawner', fillcolor='lightgreen')
        
        # User Notebook instances
        with c.subgraph(name='cluster_notebooks') as nb:
            nb.attr(label='Notebook Instances', style='rounded')
            nb.node('notebook1', 'Jupyter Notebook\nServer Pod 1', fillcolor='lightyellow')
            nb.node('notebook2', 'Jupyter Notebook\nServer Pod 2', fillcolor='lightyellow')
        
        # Storage and Configuration
        c.node('pvc', 'Persistent Volume\nClaims', fillcolor='lightpink')
        c.node('configmap', 'ConfigMap\njupyterhub_config.py', fillcolor='lightgrey')
        c.node('netpol', 'Network Policies', fillcolor='lightcoral')
        
    # External components
    dot.node('user', 'Data Science\nUsers', fillcolor='white')
    dot.node('registry', 'Container Registry\n(Custom Images)', fillcolor='white')

    # Add edges with descriptions
    dot.edge('user', 'jupyterhub', 'HTTPS')
    dot.edge('jupyterhub', 'auth', 'Authenticate')
    dot.edge('jupyterhub', 'kubespawner', 'Spawn request')
    dot.edge('kubespawner', 'notebook1', 'Create/Manage')
    dot.edge('kubespawner', 'notebook2', 'Create/Manage')
    dot.edge('notebook1', 'pvc', 'Mount storage')
    dot.edge('notebook2', 'pvc', 'Mount storage')
    dot.edge('configmap', 'jupyterhub', 'Configure')
    dot.edge('netpol', 'notebook1', 'Control traffic')
    dot.edge('netpol', 'notebook2', 'Control traffic')
    dot.edge('registry', 'notebook1', 'Pull image')
    dot.edge('registry', 'notebook2', 'Pull image')

    # Graph attributes
    dot.attr(label='\nJupyterHub on OpenShift Architecture\nDeployment and Security View', fontsize='16')
    dot.attr(fontname='Arial')
    
    return dot

# Create and save the diagram
arch = create_jupyterhub_architecture()
arch.render('jupyterhub_architecture', format='png', cleanup=True)