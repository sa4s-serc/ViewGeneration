import graphviz as gv

dot = gv.Digraph(name='Terraform_Security_Dojo_Architecture', 
                 comment='Architecture diagram for Terraform Security Dojo',
                 format='png',
                 engine='dot')

# Graph attributes
dot.attr(rankdir='TB', 
        splines='ortho',
        nodesep='0.8',
        ranksep='1.0')

# Node attributes
dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue')

# Add main components
dot.node('bootstrap', 'Bootstrap\n(VPC/Subnets)')
dot.node('iac', 'Main IaC\n(EC2/ALB/Security)')
dot.node('vscode', 'VSCode Box\n(Dev Environment)')

# Environment nodes
with dot.subgraph(name='cluster_envs') as envs:
    envs.attr(label='Environments')
    envs.node('dev', 'Development\n(dev.tfvars)')
    envs.node('prd', 'Production\n(prd.tfvars)')

# Add solutions
dot.node('solutions', 'Solution Examples\n(step_*)')

# Add edges
dot.edge('bootstrap', 'iac', 'creates infrastructure')
dot.edge('iac', 'dev', 'deploys to')
dot.edge('iac', 'prd', 'deploys to')
dot.edge('vscode', 'iac', 'develops')
dot.edge('solutions', 'iac', 'provides examples')

# Add network security emphasis
dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightpink')
dot.node('security', 'Security Components\n- Security Groups\n- Network ACLs\n- Load Balancer')

dot.edge('iac', 'security', 'implements')

if __name__ == "__main__":
    dot.render('terraform_security_dojo_architecture', view=True, cleanup=True)